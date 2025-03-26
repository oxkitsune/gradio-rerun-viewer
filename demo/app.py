import cv2
import os
import tempfile
import time

import gradio as gr
from gradio_rerun import Rerun
from gradio_rerun.events import SelectionChange, TimeUpdate, TimelineChange

import rerun as rr
import rerun.blueprint as rrb

from color_grid import build_color_grid

# NOTE: Functions that work with Rerun should be decorated with `@rr.thread_local_stream`.
# This decorator creates a generator-aware thread-local context so that rerun log calls
# across multiple workers stay isolated.


# A task can directly log to a binary stream, which is routed to the embedded viewer.
# Incremental chunks are yielded to the viewer using `yield stream.read()`.
#
# This is the preferred way to work with Rerun in Gradio since your data can be immediately and
# incrementally seen by the viewer. Also, there are no ephemeral RRDs to cleanup or manage.
@rr.thread_local_stream("rerun_example_streaming_blur")
def streaming_repeated_blur(img):
    stream = rr.binary_stream()

    if img is None:
        raise gr.Error("Must provide an image to blur.")

    blueprint = rrb.Blueprint(
        rrb.Horizontal(
            rrb.Spatial2DView(origin="image/original"),
            rrb.Spatial2DView(origin="image/blurred"),
        ),
        collapse_panels=True,
    )

    rr.send_blueprint(blueprint)

    rr.set_time_sequence("iteration", 0)

    rr.log("image/original", rr.Image(img))
    yield stream.read()

    blur = img

    for i in range(100):
        rr.set_time_sequence("iteration", i)

        # Pretend blurring takes a while so we can see streaming in action.
        time.sleep(0.1)
        blur = cv2.GaussianBlur(blur, (5, 5), 0)

        rr.log("image/blurred", rr.Image(blur))

        # Each time we yield bytes from the stream back to Gradio, they
        # are incrementally sent to the viewer. Make sure to yield any time
        # you want the user to be able to see progress.
        yield stream.read()


# However, if you have a workflow that creates an RRD file instead, you can still send it
# directly to the viewer by simply returning the path to the RRD file.
#
# This may be helpful if you need to execute a helper tool written in C++ or Rust that can't
# be easily modified to stream data directly via Gradio.
#
# In this case you may want to clean up the RRD file after it's sent to the viewer so that you
# don't accumulate too many  temporary files.
@rr.thread_local_stream("rerun_example_cube_rrd")
def create_cube_rrd(x, y, z, pending_cleanup):
    cube = build_color_grid(int(x), int(y), int(z), twist=0)
    rr.log("cube", rr.Points3D(cube.positions, colors=cube.colors, radii=0.5))

    # We eventually want to clean up the RRD file after it's sent to the viewer, so tracking
    # any pending files to be cleaned up when the state is deleted.
    temp = tempfile.NamedTemporaryFile(prefix="cube_", suffix=".rrd", delete=False)
    pending_cleanup.append(temp.name)

    blueprint = rrb.Spatial3DView(origin="cube")
    rr.save(temp.name, default_blueprint=blueprint)

    # Just return the name of the file -- Gradio will convert it to a FileData object
    # and send it to the viewer.
    return temp.name


def cleanup_cube_rrds(pending_cleanup):
    for f in pending_cleanup:
        os.unlink(f)


with gr.Blocks() as demo:
    with gr.Tab("Streaming"):
        with gr.Row():
            img = gr.Image(interactive=True, label="Image")
            with gr.Column():
                stream_blur = gr.Button("Stream Repeated Blur")
        with gr.Row():
            viewer = Rerun(
                streaming=True,
                panel_states={
                    "time": "collapsed",
                    "blueprint": "hidden",
                    "selection": "hidden",
                },
            )
        stream_blur.click(streaming_repeated_blur, inputs=[img], outputs=[viewer])

        def on_selection_change(evt: SelectionChange):
            print("selection change", evt.items)

        def on_time_update(evt: TimeUpdate):
            print("time update", evt.time)

        def on_timeline_change(evt: TimelineChange):
            print("timeline change", evt.timeline, evt.time)

        viewer.selection_change(on_selection_change)
        viewer.time_update(on_time_update)
        viewer.timeline_change(on_timeline_change)


    with gr.Tab("Dynamic RRD"):
        pending_cleanup = gr.State(
            [], time_to_live=10, delete_callback=cleanup_cube_rrds
        )
        with gr.Row():
            x_count = gr.Number(
                minimum=1, maximum=10, value=5, precision=0, label="X Count"
            )
            y_count = gr.Number(
                minimum=1, maximum=10, value=5, precision=0, label="Y Count"
            )
            z_count = gr.Number(
                minimum=1, maximum=10, value=5, precision=0, label="Z Count"
            )
        with gr.Row():
            create_rrd = gr.Button("Create RRD")
        with gr.Row():
            viewer = Rerun(
                streaming=True,
                panel_states={
                    "time": "collapsed",
                    "blueprint": "hidden",
                    "selection": "hidden",
                },
            )
        create_rrd.click(
            create_cube_rrd,
            inputs=[x_count, y_count, z_count, pending_cleanup],
            outputs=[viewer],
        )

    with gr.Tab("Hosted RRD"):
        with gr.Row():
            # It may be helpful to point the viewer to a hosted RRD file on another server.
            # If an RRD file is hosted via http, you can just return a URL to the file.
            choose_rrd = gr.Dropdown(
                label="RRD",
                choices=[
                    f"{rr.bindings.get_app_url()}/examples/arkit_scenes.rrd",
                    f"{rr.bindings.get_app_url()}/examples/dna.rrd",
                    f"{rr.bindings.get_app_url()}/examples/plots.rrd",
                ],
            )
        with gr.Row():
            viewer = Rerun(
                streaming=True,
                panel_states={
                    "time": "collapsed",
                    "blueprint": "hidden",
                    "selection": "hidden",
                },
            )
        choose_rrd.change(lambda x: x, inputs=[choose_rrd], outputs=[viewer])


if __name__ == "__main__":
    demo.launch()


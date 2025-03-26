
import gradio as gr
from app import demo as app
import os

_docs = {'Rerun': {'description': 'Creates a Rerun viewer component that can be used to display the output of a Rerun stream.', 'members': {'__init__': {'value': {'type': 'typing.Union[\n    list[pathlib.Path | str],\n    pathlib.Path,\n    str,\n    bytes,\n    typing.Callable,\n    NoneType,\n][\n    list[pathlib.Path | str],\n    pathlib.Path,\n    str,\n    bytes,\n    Callable,\n    None,\n]', 'default': 'None', 'description': 'Takes a singular or list of RRD resources. Each RRD can be a Path, a string containing a url, or a binary blob containing encoded RRD data. If callable, the function will be called whenever the app loads to set the initial value of the component.'}, 'label': {'type': 'str | None', 'default': 'None', 'description': 'The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.'}, 'every': {'type': 'float | None', 'default': 'None', 'description': "If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. Queue must be enabled. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute."}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display label.'}, 'container': {'type': 'bool', 'default': 'True', 'description': 'If True, will place the component in a container - providing some extra padding around the border.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'height': {'type': 'int | str', 'default': '640', 'description': 'height of component in pixels. If a string is provided, will be interpreted as a CSS value. If None, will be set to 640px.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'streaming': {'type': 'bool', 'default': 'False', 'description': 'If True, the data should be incrementally yielded from the source as `bytes` returned by calling `.read()` on an `rr.binary_stream()`'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'panel_states': {'type': 'dict[str, typing.Any] | None', 'default': 'None', 'description': 'Force viewer panels to a specific state. Any panels set cannot be toggled by the user in the viewer. Panel names are "top", "blueprint", "selection", and "time". States are "hidden", "collapsed", and "expanded".'}}, 'postprocess': {'value': {'type': 'list[pathlib.Path | str] | pathlib.Path | str | bytes', 'description': 'Expects'}}, 'preprocess': {'return': {'type': 'RerunData | None', 'description': 'A RerunData object.'}, 'value': None}}, 'events': {'selection_change': {'type': None, 'default': None, 'description': 'Fired when the selection changes.'}, 'time_update': {'type': None, 'default': None, 'description': 'Fired when time updates.'}, 'timeline_change': {'type': None, 'default': None, 'description': 'Fired when a timeline is selected.'}}}, '__meta__': {'additional_interfaces': {}}, 'SelectionChange': {'description': 'When gr.EventData or one of its subclasses is added as a type hint to an argument of a prediction function, a gr.EventData object will automatically be passed as the value of that argument.\nThe attributes of this object contains information about the event that triggered the listener. The gr.EventData object itself contains a `.target` attribute that refers to the component\nthat triggered the event, while subclasses of gr.EventData contains additional attributes that are different for each class.\n\n    import gradio as gr\n    with gr.Blocks() as demo:\n        table = gr.Dataframe([[1, 2, 3], [4, 5, 6]])\n        gallery = gr.Gallery([("cat.jpg", "Cat"), ("dog.jpg", "Dog")])\n        textbox = gr.Textbox("Hello World!")\n        statement = gr.Textbox()\n        def on_select(value, evt: gr.EventData):\n            return f"The {evt.target} component was selected, and its value was {value}."\n        table.select(on_select, table, statement)\n        gallery.select(on_select, gallery, statement)\n        textbox.select(on_select, textbox, statement)\n    demo.launch()', 'members': {'__init__': {'target': {'type': 'typing.Any', 'description': 'The component object that triggered the event. Can be used to distinguish multiple components bound to the same listener.'}, 'data': {'type': 'typing.Any', 'description': None}}}, 'events': {}}, 'TimeUpdate': {'description': 'When gr.EventData or one of its subclasses is added as a type hint to an argument of a prediction function, a gr.EventData object will automatically be passed as the value of that argument.\nThe attributes of this object contains information about the event that triggered the listener. The gr.EventData object itself contains a `.target` attribute that refers to the component\nthat triggered the event, while subclasses of gr.EventData contains additional attributes that are different for each class.\n\n    import gradio as gr\n    with gr.Blocks() as demo:\n        table = gr.Dataframe([[1, 2, 3], [4, 5, 6]])\n        gallery = gr.Gallery([("cat.jpg", "Cat"), ("dog.jpg", "Dog")])\n        textbox = gr.Textbox("Hello World!")\n        statement = gr.Textbox()\n        def on_select(value, evt: gr.EventData):\n            return f"The {evt.target} component was selected, and its value was {value}."\n        table.select(on_select, table, statement)\n        gallery.select(on_select, gallery, statement)\n        textbox.select(on_select, textbox, statement)\n    demo.launch()', 'members': {'__init__': {'target': {'type': 'typing.Any', 'description': 'The component object that triggered the event. Can be used to distinguish multiple components bound to the same listener.'}, 'data': {'type': 'typing.Any', 'description': None}}}, 'events': {}}, 'TimelineChange': {'description': 'When gr.EventData or one of its subclasses is added as a type hint to an argument of a prediction function, a gr.EventData object will automatically be passed as the value of that argument.\nThe attributes of this object contains information about the event that triggered the listener. The gr.EventData object itself contains a `.target` attribute that refers to the component\nthat triggered the event, while subclasses of gr.EventData contains additional attributes that are different for each class.\n\n    import gradio as gr\n    with gr.Blocks() as demo:\n        table = gr.Dataframe([[1, 2, 3], [4, 5, 6]])\n        gallery = gr.Gallery([("cat.jpg", "Cat"), ("dog.jpg", "Dog")])\n        textbox = gr.Textbox("Hello World!")\n        statement = gr.Textbox()\n        def on_select(value, evt: gr.EventData):\n            return f"The {evt.target} component was selected, and its value was {value}."\n        table.select(on_select, table, statement)\n        gallery.select(on_select, gallery, statement)\n        textbox.select(on_select, textbox, statement)\n    demo.launch()', 'members': {'__init__': {'target': {'type': 'typing.Any', 'description': 'The component object that triggered the event. Can be used to distinguish multiple components bound to the same listener.'}, 'data': {'type': 'typing.Any', 'description': None}}}, 'events': {}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_rerun`

<div style="display: flex; gap: 7px;">
<a href="https://pypi.org/project/gradio_rerun/" target="_blank"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/gradio_rerun"></a> <a href="https://github.com/radames/gradio-rerun-viewer/issues" target="_blank"><img alt="Static Badge" src="https://img.shields.io/badge/Issues-white?logo=github&logoColor=black"></a> 
</div>

Rerun viewer with Gradio
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_rerun
```

## Usage

```python
import cv2
import os
import tempfile
import time

import gradio as gr
from gradio_rerun import Rerun, SelectionChange, TimeUpdate, TimelineChange

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

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `Rerun`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["Rerun"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["Rerun"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, a RerunData object.
- **As output:** Should return, expects.

 ```python
def predict(
    value: RerunData | None
) -> list[pathlib.Path | str] | pathlib.Path | str | bytes:
    return value
```
""", elem_classes=["md-custom", "Rerun-user-fn"], header_links=True)


    gr.Markdown("""
## `SelectionChange`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["SelectionChange"]["members"]["__init__"], linkify=[])





    gr.Markdown("""
## `TimeUpdate`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["TimeUpdate"]["members"]["__init__"], linkify=[])





    gr.Markdown("""
## `TimelineChange`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["TimelineChange"]["members"]["__init__"], linkify=[])







    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {};
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()

<svelte:options accessors={true} />

<script context="module" lang="ts">
  export { default as BaseExample } from "./Example.svelte";
</script>

<script lang="ts">
  import "./app.css";
  import type { Gradio } from "@gradio/utils";
  import {
    LogChannel,
    WebViewer,
    type Panel,
    type PanelState,
  } from "@rerun-io/web-viewer";
  import { onMount } from "svelte";
  import { Block } from "@gradio/atoms";
  import { StatusTracker } from "@gradio/statustracker";
  import type { FileData } from "@gradio/client";
  import type { LoadingStatus } from "@gradio/statustracker";
  import type { SelectionItem } from "@rerun-io/web-viewer";

  interface BinaryStream {
    url: string;
    is_stream: boolean;
  }

  export let elem_id = "";
  export let elem_classes: string[] = [];
  export let visible = true;
  export let height: number | string = 640;
  export let value: null | BinaryStream | (FileData | string)[] = null;
  export let container = true;
  export let scale: number | null = null;
  export let min_width: number | undefined = undefined;
  export let loading_status: LoadingStatus;
  export let interactive: boolean;
  export let streaming: boolean;
  export let panel_states: { [K in Panel]: PanelState } | null = null;

  let old_value: null | BinaryStream | (FileData | string)[] = null;
  export let gradio: Gradio<{
    change: never;
    upload: never;
    clear: never;
    clear_status: LoadingStatus;
    selection_change: SelectionItem[];
    time_update: number;
    timeline_change: {timeline: string, time: number};
  }>;

  $: height = typeof height === "number" ? `${height}px` : height;

  let dragging: boolean;
  let rr: WebViewer;
  let channel: LogChannel;
  let ref: HTMLDivElement;
  let patched_loading_status: LoadingStatus;

  // Global set to track segments already sent
  let sentSegments = new Set<string>();

  function try_load_value() {
    if (rr != undefined && rr.ready) {
      old_value = value;
      if (!Array.isArray(value)) {
        if (value.is_stream) {
          // Fetch the HLS playlist
          fetch(value.url)
            .then((response) => {
              if (!response.ok) throw new Error("Failed to fetch playlist");
              return response.text();
            })
            .then((playlistContent) => {
              // Parse the playlist to extract segment URLs
              const lines = playlistContent.trim().split("\n");
              const baseUrl = new URL("./", value.url).href;
              const uniqueSegmentUrls: string[] = [];

              // Only include segments that haven't been processed yet
              lines.forEach((line) => {
                if (!line.startsWith("#") && line.trim()) {
                  const segmentUrl = line.startsWith("http")
                    ? line
                    : new URL(line, baseUrl).href;
                  if (!sentSegments.has(segmentUrl)) {
                    uniqueSegmentUrls.push(segmentUrl);
                  }
                }
              });

              // Fetch and process each segment sequentially
              let processedCount = 0;
              function processNextSegment() {
                if (processedCount >= uniqueSegmentUrls.length) {
                  return;
                }
                const currentUrl = uniqueSegmentUrls[processedCount];

                // Extra check in case the segment was processed in a previous run
                if (sentSegments.has(currentUrl)) {
                  processedCount++;
                  processNextSegment();
                  return;
                }

                fetch(currentUrl)
                  .then((response) => {
                    if (!response.ok)
                      throw new Error(`Failed to fetch segment: ${currentUrl}`);
                    return response.arrayBuffer();
                  })
                  .then((buffer) => {
                    channel.send_rrd(new Uint8Array(buffer));

                    sentSegments.add(currentUrl);
                    processedCount++;
                    processNextSegment();
                  })
                  .catch((error) => {
                    console.error(
                      `Error processing segment ${currentUrl}:`,
                      error
                    );
                    processedCount++;
                    processNextSegment();
                  });
              }
              processNextSegment();
            })
            .catch((error) => {
              console.error("Error fetching or processing HLS stream:", error);
            });
        } else {
          rr.open(value.url);
        }
      } else {
        for (const file of value) {
          if (typeof file !== "string") {
            if (file.url) {
              rr.open(file.url);
            }
          } else {
            rr.open(file);
          }
        }
      }
    }
  }

  const is_panel = (v: string): v is Panel =>
    ["top", "blueprint", "selection", "time"].includes(v);

  function setup_panels() {
    if (rr?.ready && panel_states) {
      for (const panel in panel_states) {
        if (!is_panel(panel)) continue;
        rr.override_panel_state(panel, panel_states[panel]);
      }
    }
  }

  onMount(() => {
    rr = new WebViewer();
    rr.on("ready", () => {
      channel = rr.open_channel("gradio");
      try_load_value();
      setup_panels();
    });
    rr.on("fullscreen", (on) => rr.toggle_panel_overrides(!on));
    rr.on("selectionchange", (items) => gradio.dispatch("selection_change", items));
    rr.on("timeupdate", (time) => gradio.dispatch("time_update", time));
    rr.on("timelinechange", (timeline, time) => gradio.dispatch("timeline_change", {timeline,time}));

    rr.start(undefined, ref, {
      hide_welcome_screen: true,
      allow_fullscreen: true,
      width: "",
      height: "",
    });
    return () => {
      channel = null;
      rr.stop();
    };
  });

  $: {
    patched_loading_status = loading_status;
    if (streaming && patched_loading_status?.status === "generating") {
      patched_loading_status.status = "complete";
    }
  }

  $: value, try_load_value();
  $: panel_states, setup_panels();
</script>

{#if !interactive}
  <Block
    {visible}
    variant={"solid"}
    border_mode={dragging ? "focus" : "base"}
    padding={false}
    {elem_id}
    {elem_classes}
    allow_overflow={false}
    {container}
    {scale}
    {min_width}
  >
    <StatusTracker
      autoscroll={gradio.autoscroll}
      i18n={gradio.i18n}
      {...patched_loading_status}
      on:clear_status={() => gradio.dispatch("clear_status", loading_status)}
    />
    <div class="viewer" bind:this={ref} style:height />
  </Block>
{/if}

<style lang="scss">
  div.viewer {
    width: 100%;
    :global(> canvas) {
      display: block;
      width: 100%;
      height: 100%;
    }
  }
</style>

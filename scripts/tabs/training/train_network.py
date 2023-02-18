import argparse

import gradio as gr

from kohya_ss.library import train_util
from scripts import presets, ui
from scripts.runner import initialize_runner
from scripts.utils import args_to_gradio, load_args_template, options_to_gradio


def title():
    return "Train network"


def create_ui():
    sd_models_arguments = argparse.ArgumentParser()
    dataset_arguments = argparse.ArgumentParser()
    training_arguments = argparse.ArgumentParser()
    train_util.add_sd_models_arguments(sd_models_arguments)
    train_util.add_dataset_arguments(dataset_arguments, True, True, True)
    train_util.add_training_arguments(training_arguments, True)
    sd_models_options = {}
    dataset_options = {}
    training_options = {}
    network_options = {}

    templates, script_file = load_args_template("train_network.py")

    get_options = lambda: {
        **sd_models_options,
        **dataset_options,
        **training_options,
        **network_options,
    }

    get_templates = lambda: {
        **sd_models_arguments.__dict__["_option_string_actions"],
        **dataset_arguments.__dict__["_option_string_actions"],
        **training_arguments.__dict__["_option_string_actions"],
        **templates,
    }

    with gr.Column():
        init_runner = initialize_runner(script_file, get_templates, get_options)
        with gr.Box():
            with gr.Row():
                init_id = presets.create_ui("train_network", get_templates, get_options)
        with gr.Row():
            with gr.Group():
                with gr.Box():
                    ui.title("Network options")
                    options_to_gradio(
                        templates,
                        network_options,
                        {
                            "network_module": {
                                "type": list,
                                "choices": ["networks.lora"],
                            }
                        },
                    )
                with gr.Box():
                    ui.title("Model options")
                    args_to_gradio(sd_models_arguments, sd_models_options)
                with gr.Box():
                    ui.title("Dataset options")
                    args_to_gradio(dataset_arguments, dataset_options)
            with gr.Box():
                ui.title("Trianing options")
                args_to_gradio(training_arguments, training_options)

    init_runner()
    init_id()

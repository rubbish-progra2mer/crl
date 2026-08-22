import datetime
import os

import datasets as ds
from dataclasses import dataclass

from huggingface_hub import HfApi

TOKEN = os.environ.get("TOKEN", None)

api = HfApi()


@dataclass
class Experiment:
    path_to_hub: str
    organisation: str
    model: str
    cur_date: str = str(datetime.datetime.today().strftime('%Y-%m-%d-%H-%M'))

    def __str__(self):
        return f"{self.organisation}_{self.model}_{self.cur_date}"


def format_error(msg):
    return f"<p style='color: red; font-size: 20px; text-align: center;'>{msg}</p>"

def format_warning(msg):
    return f"<p style='color: orange; font-size: 20px; text-align: center;'>{msg}</p>"

def format_log(msg):
    return f"<p style='color: green; font-size: 20px; text-align: center;'>{msg}</p>"

def model_hyperlink(link, model_name):
    return f'<a target="_blank" href="{link}" style="color: var(--link-text-color); text-decoration: underline;text-decoration-style: dotted;">{model_name}</a>'

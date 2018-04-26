from flask import request, current_app
import tensorflow as tf
import numpy as np
from io import StringIO

def main():
	msg = "We arrived here!?"
	payload = request.get_json(force=True)
	data = payload["data"]
	return data
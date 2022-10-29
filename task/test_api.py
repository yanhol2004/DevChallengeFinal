from fastapi.testclient import TestClient
from api import app
import base64

client = TestClient(app)

def test_4_black_cells():
	"""grid with 4 completely black cells."""
	with open("test_images/4blackcells.png", "rb") as image_file:
		img_base64 = base64.b64encode(image_file.read())
	img_base64 = img_base64.decode("utf-8")

	response = client.post("api/image-input", json={
			"min_level": 10,
  			"image": img_base64
		}
	)

	assert response.status_code == 200
	assert response.json() == [
	{
		"x": 0,
		"y": 0,
		"level": 100
	},
	{
		"x": 1,
		"y": 0,
		"level": 100
	},
	{
		"x": 0,
		"y": 1,
		"level": 100
	},
	{
		"x": 1,
		"y": 1,
		"level": 100
	}
	]

def test_no_grid():
	"""image with no grid"""
	with open("test_images/without_grid.png", "rb") as image_file:
		img_base64 = base64.b64encode(image_file.read())
	img_base64 = img_base64.decode("utf-8")

	response = client.post("api/image-input", json={
			"min_level": 20,
  			"image": img_base64
		}
	)

	assert response.status_code == 422
	assert response.json() == {
		"error": "string",
		"details": "The provided image has no grid."
	}

def test_invalid_min_level():
	"""checking error handling when min_level is invalid"""
	with open("test_images/without_grid.png", "rb") as image_file:
		img_base64 = base64.b64encode(image_file.read())
	img_base64 = img_base64.decode("utf-8")

	response = client.post("api/image-input", json={
			"min_level": -1,
  			"image": img_base64
		}
	)

	assert response.status_code == 422
	assert response.json() == {
		"error": "string",
		"details": "Invalid provided minimum level data."
	}

def test_invalid_image_data():
	"""checking error handling with invalid image data"""
	img_base64 = "some string"

	response = client.post("api/image-input", json={
			"min_level": 10,
  			"image": img_base64
		}
	)

	assert response.status_code == 422
	assert response.json() == {
		"error": "string",
		"details": "Unprocessable image."
	}

def test_dummy_gridlines():
	"""the image provided has many horizontal and vertical lines,
	that are not the gridlines"""
	with open("test_images/dummy_gridlines.png", "rb") as image_file:
		img_base64 = base64.b64encode(image_file.read())
	img_base64 = img_base64.decode("utf-8")

	response = client.post("api/image-input", json={
			"min_level": 60,
  			"image": img_base64
		}
	)

	assert response.status_code == 200
	assert response.json() == [
	{
		"x": 0,
		"y": 1,
		"level": 75
	},
	{
		"x": 1,
		"y": 1,
		"level": 100
	},
	{
		"x": 2,
		"y": 1,
		"level": 100
	},
	{
		"x": 3,
		"y": 1,
		"level": 100
	},
	{
		"x": 0,
		"y": 2,
		"level": 75
	},
	{
		"x": 1,
		"y": 2,
		"level": 100
	},
	{
		"x": 2,
		"y": 2,
		"level": 100
	},
	{
		"x": 3,
		"y": 2,
		"level": 100
	},
	{
		"x": 0,
		"y": 3,
		"level": 75
	},
	{
		"x": 1,
		"y": 3,
		"level": 100
	},
	{
		"x": 2,
		"y": 3,
		"level": 100
	},
	{
		"x": 3,
		"y": 3,
		"level": 100
	}
	]


def test_many_white_pixels():
	"""grid with lots of white pixels."""
	with open("test_images/many_white_pixels.png", "rb") as image_file:
		img_base64 = base64.b64encode(image_file.read())
	img_base64 = img_base64.decode("utf-8")

	response = client.post("api/image-input", json={
			"min_level": 10,
  			"image": img_base64
		}
	)

	assert response.status_code == 200
	assert response.json() == [
	{
		"x": 0,
		"y": 0,
		"level": 33
	},
	{
		"x": 1,
		"y": 0,
		"level": 33
	},
	{
		"x": 0,
		"y": 1,
		"level": 33
	},
	{
		"x": 1,
		"y": 1,
		"level": 33
	}
	]

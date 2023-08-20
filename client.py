import requests

# response = requests.post(
#     "http://127.0.0.1:5000/ads/",
#     json={"header": "test", "description": "text", "user_name": "user_1"},
# )
#
# print(response.status_code)
# print(response.text)


# response = requests.get(
#     "http://127.0.0.1:5000/ads/1"
# )
#
# print(response.status_code)
# print(response.text)


response = requests.delete("http://127.0.0.1:5000/ads/1")

print(response.status_code)
print(response.text)

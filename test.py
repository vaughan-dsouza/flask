import requests

BASE = "http://127.0.0.1:5000/"

# data = [{"likes": 78, "name": "Joe", "views":152100 },
#         {"likes": 1000, "name": "How to make your api", "views":800000 },
#         {"likes": 35, "name": "Tim", "views":65200 }]

# for i in range(len(data)):
#     response = requests.put(BASE + "video/" + str(i), data[i])
#     print(response.json())

# input()
# response = requests.delete(BASE + "video/")
# print(response)
# input()
# response = requests.get(BASE + "video/2")
# print(response.json())

response = requests.patch(BASE + "video/2", {"views": 99, "likes": 505})
print(response.json())
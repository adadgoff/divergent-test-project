import json
import os.path

from flask import Flask, jsonify, abort

app = Flask(__name__)


def data_loader() -> tuple[list, list]:
    """
    Функция загружает данные из json файлов и преобразует их в list.
    Функция не должна нарушать изначальную структуру данных.
    """
    base_path = os.path.dirname(__file__)
    comments_path = os.path.join(base_path, "data", "comments.json")
    posts_path = os.path.join(base_path, "data", "posts.json")

    with (open(comments_path, mode="r", encoding="utf-8") as comments_f,
          open(posts_path, mode="r", encoding="utf-8") as posts_f):
        comments = json.load(comments_f)
        posts = json.load(posts_f)

    return posts["posts"], comments["comments"]


@app.route("/")
def get_posts():
    """
    На странице / вывести json в котором каждый элемент - это:
    - пост из файла posts.json.
    - для каждой поста указано кол-во комментариев этого поста из файла comments.json

    Формат ответа:
    posts: [
        {
            id: <int>,
            title: <str>,
            body: <str>, 
            author:	<str>,
            created_at: <str>,
            comments_count: <int>
        }
    ],
    total_results: <int>

    Порядок ключей словаря в ответе не важен
    """
    posts, comments = data_loader()

    output_posts = [
        {
            **post,
            "comments_count": sum(comment["post_id"] == post["id"] for comment in comments),
        }
        for post in posts
    ]

    output = {
        "posts": output_posts,
        "total_results": len(output_posts),
    }

    return jsonify(output)


@app.route("/posts/<int:post_id>")
def get_post(post_id):
    """
    На странице /posts/<post_id> вывести json, который должен содержать:
    - пост с указанным в ссылке id
    - список всех комментариев к новости

    Отдавайте ошибку abort(404), если пост не существует.


    Формат ответа:
    id: <int>,
    title: <str>,
    body: <str>, 
    author:	<str>,
    created_at: <str>
    comments: [
        "user": <str>,
        "post_id": <int>,
        "comment": <str>,
        "created_at": <str>
    ]

    Порядок ключей словаря в ответе не важен
    """
    posts, comments = data_loader()

    output_post = next((post for post in posts if post["id"] == post_id), None)

    if not output_post:
        abort(status=404)

    output_post["comments"] = [comment for comment in comments if comment["post_id"] == post_id]

    output = {"post": output_post}

    return jsonify(output)

from flask import Flask, jsonify, request
from flask.views import MethodView

from models import Ads, Session

app = Flask("app")


class HttpError(Exception):
    def __init__(self, status_code: int, message: dict | str | list):
        self.status_code = status_code
        self.message = message


def ads_get(ads_id: int, session: Session):
    ads = session.get(Ads, ads_id)
    if ads is None:
        raise HttpError(404, "advertisement not found")
    return ads


class AdsView(MethodView):
    def get(self, ads_id):
        with Session() as session:
            ads = ads_get(ads_id, session)
            return jsonify(
                {
                    "id": ads.id,
                    "header": ads.header,
                    "description": ads.description,
                    "user_name": ads.user_name,
                    "creation_time": ads.creation_time,
                }
            )

    def post(self):
        with Session() as session:
            new_ads = Ads(**request.json)
            session.add(new_ads)
            session.commit()
            return jsonify({"id": new_ads.id})

    def patch(self, ads_id):
        with Session() as session:
            ads = ads_get(ads_id, session)
            for key, value in request.json.items():
                setattr(ads, key, value)
            session.add(ads)
            session.commit()
            return jsonify({"status": "success"})

    def delete(self, ads_id):
        with Session() as session:
            ads = ads_get(ads_id, session)
            session.delete(ads)
            session.commit()
            return jsonify({"status": "success"})


ads_view = AdsView.as_view("ads")

app.add_url_rule("/ads/", view_func=ads_view, methods=["POST"])
app.add_url_rule(
    "/ads/<int:ads_id>", view_func=ads_view, methods=["GET", "PATCH", "DELETE"]
)


if __name__ == "__main__":
    app.run()

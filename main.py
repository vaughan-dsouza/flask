from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    views = db.Column(db.Integer, nullable = False)
    likes = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Video(name = {name}, views = {views}, likes = {likes})"

# db.create_all()
 
# names = {"vaughan" : {"age":19, "gender": "male"},
#         "tim" : {"age":22, "gender": "male"}
# }
video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name the video", required=True)
video_put_args.add_argument("views", type=int, help="views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="likes of the video", required=True)

video_update_args = reqparse.RequestParser()
video_update_args.add_argument("name", type=str, help="Name the video")
video_update_args.add_argument("views", type=int, help="views of the video")
video_update_args.add_argument("likes", type=int, help="likes of the video")

# videos = {}

# def abort_if_not_exist(video_id):
#     if video_id not in videos:
#         abort(404, message="video does not exist")

# def abort_if_exist(video_id):
#     if video_id in videos:
#         abort(409, message="video does already exist")

resource_fields = {
    'id' : fields.Integer,
    'name' : fields.String,
    'views' : fields.Integer,
    'likes' : fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        # abort_if_not_exist(video_id)
        # return videos[video_id]
        result = VideoModel.query.filter_by(id=video_id).first()
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        # print(request.form["likes"])
        args = video_put_args.parse_args()
        # videos[video_id] = args 
        # return videos[video_id], 201
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="video id taken...")
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video doesn't exist, cannot update")
        if args['name']:
            result.name = args['name']
        if args['views']:
            result.views = args['views']
        if args['likes']:
            result.likes = args['likes']
        
        # once in da no need for add statement
        # db.session.add(result)
        db.session.commit()

        return result


    def delete(self, video_id):
        abort_if_not_exist(video_id)
        del video[video_id]
        return '', 204

api.add_resource(Video, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True, port=5001)


from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import content_recommender

# Khởi tạo ứng dụng Flask
app = Flask(__name__)

# Áp dụng CORS
CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"


# API endpoint để gợi ý nội dung dựa trên tiêu đề phim
@app.route("/recommend", methods=["GET"])
@cross_origin(origin="*")
def recommend_content():
    movie_title = request.args.get("title")  # Lấy tiêu đề phim từ request
    recommendations = content_recommender.content_recommender(movie_title)
    return jsonify(recommendations.tolist())  # Trả về danh sách gợi ý dưới dạng JSON


@app.route("/", methods=["GET"])
@cross_origin(origin="*")
def hello():
    return "Xin chào"


# Khởi chạy ứng dụng Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="9999")

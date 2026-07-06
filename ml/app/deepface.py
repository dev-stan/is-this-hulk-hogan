import logging
from deepface import DeepFace
import numpy as np

logger = logging.getLogger(__name__)


def compare_faces(user_path: str, char_path: str) -> dict:
    """
    Compare a user's face to a character's face using DeepFace.

    Returns a dict of raw prediction data
    """
    logger.info("Comparing image %s against %s", user_path, char_path)

    DeepFace.build_model("ArcFace")

    try:
        result = DeepFace.verify(
            img1_path=user_path,
            img2_path=char_path,
            model_name="VGG-Face",
            detector_backend="opencv",
            enforce_detection=True,
        )

        distance = result["distance"]

        logger.info(
            "Comparison result — distance: %.4f",
            distance,
        )

        return {
            "distance": round(distance, 4),
        }

    except Exception:
        logger.exception(
            "Face comparison failed for %s vs %s", user_path, char_path
        )
        raise
    
EMOTIONS = ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]


def compare_emotions(user_path: str, char_path: str) -> dict:
    """
    Compare the emotional expression of a user's face to a character's face.

    Returns raw prediction data emotion vectors + cosine similarity
    """
    logger.info("Comparing emotions: %s vs %s", user_path, char_path)

    try:
        user_emotions = DeepFace.analyze(
            img_path=user_path,
            actions=["emotion"],
            detector_backend="opencv",
        )[0]["emotion"]

        char_emotions = DeepFace.analyze(
            img_path=char_path,
            actions=["emotion"],
            detector_backend="opencv",
        )[0]["emotion"]

        logger.info("User emotions: %s", user_emotions)
        logger.info("Character emotions: %s", char_emotions)

        # Compare emotion distributions using cosine similarity between vectors
        vec_user = np.array([user_emotions[e] for e in EMOTIONS])
        vec_char = np.array([char_emotions[e] for e in EMOTIONS])

        cosine_similarity = np.dot(vec_user, vec_char) / (
            np.linalg.norm(vec_user) * np.linalg.norm(vec_char)
        )
        similarity_percent = round(float(cosine_similarity) * 100, 1)

        logger.info("Emotion similarity: %.1f%%", similarity_percent)

        return {
            "user_emotions": user_emotions,
            "char_emotions": char_emotions,
            "similarity_percent": similarity_percent,
        }

    except Exception:
        logger.exception(
            "Emotion comparison failed for %s vs %s", user_path, char_path
        )
        raise
    
    
def main(user_path: str, char_path: str) -> dict:
    """
    Compare a user's face to a character's face on both identity
    and emotional expression.

    Returns a combined, clean result dict.
    """
    face_result = compare_faces(user_path, char_path)
    emotion_result = compare_emotions(user_path, char_path)

    return {
        "face": {
            "distance": face_result["distance"],
        },
        "emotion": {
            "similarity_percent": emotion_result["similarity_percent"],
            "user_emotions": emotion_result["user_emotions"],
            "char_emotions": emotion_result["char_emotions"],
        },
    }
"""
Part 5 - Integrated Waste Management Assistant   [Owner: Teddy]

Ties the three models together behind one entry point. Takes EITHER an image
path OR a text description, classifies the waste, then generates recycling
instructions grounded in the retrieved policy documents.
"""
from . import config as C
from . import cnn_model, text_classifier, rag_system


def assist(image_path=None, description=None, query=None):
    """
    Unified assistant.
      - image_path: classify with the CNN (Part 2)
      - description: classify with the text model (Part 3)
    Then generate instructions via RAG (Part 4).
    Returns a dict with the prediction, instructions, and the policy docs used.
    """
    if not image_path and not description:
        raise ValueError("Provide either image_path or description.")

    if image_path:
        category = cnn_model.predict_image(image_path)
        modality = "image"
    else:
        category = text_classifier.predict_text(description)
        modality = "text"

    if category not in C.CATEGORIES:
        return {"ok": False, "error": f"Unknown category '{category}'"}

    instructions, docs = rag_system.generate_instructions(category, query)
    return {
        "ok": True,
        "modality": modality,
        "predicted_category": category,
        "recycling_instructions": instructions,
        "policy_sources": [d["source"] for d in docs],
        "retrieved_docs": docs,
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(assist(description=" ".join(sys.argv[1:])))

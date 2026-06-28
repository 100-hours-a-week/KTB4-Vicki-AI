from src.vector_store_manager import VectorStoreManager


def main():
    manager = VectorStoreManager()
    manager.build_vectorstore()


if __name__ == "__main__":
    print("Start ingest")
    main()
    print("Done")

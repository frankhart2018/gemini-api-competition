from user_matching_service.queue import UserMatchingConsumer


def main():
    queue = UserMatchingConsumer()

    try:
        print("Starting to listen to the queue")
        queue.start_listening()
    except KeyboardInterrupt:
        queue.stop_listening()


if __name__ == "__main__":
    main()

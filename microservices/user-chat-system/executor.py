from user_chat_system.queue.consumer import UserChatConsumer


def main():
    consumer = UserChatConsumer()

    try:
        consumer.start_listening()
    except KeyboardInterrupt:
        consumer.stop_listening()


if __name__ == "__main__":
    main()

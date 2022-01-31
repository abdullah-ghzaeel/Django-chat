import pika


def consumer():
    # credentials = pika.PlainCredentials('admin', 'admin')
    parameters = pika.ConnectionParameters(host="localhost")
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.exchange_declare(exchange="topic_logs", exchange_type="topic")
    result = channel.queue_declare("")
    queue_name = "task_queue"
    binding_key = ""
    channel.queue_bind(
        exchange="topic_logs", queue=queue_name, routing_key="task_queue"
    )
    print(" [*] Waiting for logs. To exit press CTRL+C")
    # method,properties,mes = channel.basic_get(queue=queue_name,  auto_ack=True)
    # global message
    # message = mes
    # channel.start_consuming()
    # if (message == None):
    # return "Queue empty"
    # else :
    # return message
    global message
    messages = []
    for method_frame, properties, body in channel.consume(
        queue_name, inactivity_timeout=3,auto_ack=True
    ):
        # Display the message parts
        # print(method_frame)
        print("\n\n\nMessage:")
        print(body)
        print(method_frame)
        print("end message")
        if method_frame != None:
            messages.append(
                {
                    "body": body.decode("utf-8"),
                    "properties": properties,
                }
            )
        else:
            print("Stopping")
            # channel.stop_consuming()
            channel.close()
            # connection.close()
            return messages
    channel.stop_consuming()
    channel.close()
    # connection.close()
    return messages

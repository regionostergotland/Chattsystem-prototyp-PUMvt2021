from chatbot.prepDB import prepare_db
import server_setup

# Starts the server
app = server_setup.app
if __name__ == '__main__':
    server_setup.run()

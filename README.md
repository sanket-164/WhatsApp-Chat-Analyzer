# WhatsApp Chat Analyzer (<a href="https://sanket-s-whatsapp-chat-analyzer.streamlit.app/" target="__blank">**View**</a>)

Analyze your WhatsApp conversations with ease. This tool provides insights into message counts, media sharing, word usage, and activity trends using Python, Pandas, Streamlit, and Matplotlib.  

## Features  
- **Message Statistics** : Count messages, words, media, and links  
- **Top Users** : Identify the most active participants in group chats  
- **Timeline Analysis** : Visualize chat activity over time  
- **Interactive UI** : Simple & intuitive interface powered by Streamlit  

## Tech Stack  
- **Python** : Backend processing  
- **Pandas** : Data manipulation  
- **Matplotlib** : Data visualization  
- **Streamlit** : Web-based UI  

## Setup & Installation  

1. Clone the Repository  
```bash
git clone https://github.com/sanket-164/WhatsApp-Chat-Analyzer.git
```

2. Navigate to project directory
```bash
cd Whatsapp-Chat-Analyzer
```

3. Install Dependencies  
```bash
pip install -r requirements.txt
```

4. Run the App  
```bash
streamlit run app.py
```

## Running with Docker  

1. Pull the Docker image  

```bash
docker pull sanket164/whatsapp-chat-analyzer
```

2. Run the Docker container
```bash
docker run -d -p 8501:8501 --name whatsapp-chat-analyzer sanket164/whatsapp-chat-analyzer
```
   - `-d` runs the container in detached mode.
   - `-p 8501:8501` maps the container's port 8501 to your local machine.
   - `--name whatsapp-chat-analyzer` assigns a name to the container.

3. Open your browser and visit
```
http://localhost:8501
```

4. To stop and remove the container
```bash
docker stop whatsapp-chat-analyzer
```

5. To remove the container
```bash
docker rm whatsapp-chat-analyzer
```

## How to Use  
1. Export your WhatsApp chat (`.txt` format).  
2. Upload the chat file in the Streamlit app.  
3. View insights & graphs instantly.  

## License  
This project is open-source under the [MIT License](LICENSE).  

## Contribute  
Have ideas or improvements? Feel free to fork the repo & submit a pull request.


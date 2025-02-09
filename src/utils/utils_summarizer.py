import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import re
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
import requests
from bs4 import BeautifulSoup

def get_video_id(url):
    """Extract video ID from any YouTube URL format"""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'youtu\.be\/([0-9A-Za-z_-]{11})',
        r'(?:embed\/)([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_auto_transcript(video_id):
    """Attempt to retrieve the auto-generated transcript"""
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        for lang in ['pt', 'pt-BR', 'en']:
            try:
                transcript = transcript_list.find_generated_transcript([lang])
                return ' '.join([t['text'] for t in transcript.fetch()])
            except NoTranscriptFound:
                continue
        
        for transcript in transcript_list:
            if transcript.is_generated:
                return ' '.join([t['text'] for t in transcript.fetch()])
    except (NoTranscriptFound, TranscriptsDisabled):
        return None
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return None

def get_video_info(video_id):
    """Retrieve video title and description"""
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, 'html.parser')
        
        title = soup.find('meta', property='og:title')
        title = title['content'] if title else "Título não encontrado"
        
        description = soup.find('meta', property='og:description')
        description = description['content'] if description else ""
        
        return title, description
    except:
        return "Título não encontrado", ""

def summarize_video(link, api_key):
    """
    Extracts the transcript, retrieves video info, and generates a summary.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    video_id = get_video_id(link)
    if not video_id:
        return "Erro: URL do YouTube inválida. Por favor, verifique o link."
    
    title, description = get_video_info(video_id)
    transcript = get_auto_transcript(video_id)
    
    if not transcript:
        return ("Erro: Não foi possível extrair a transcrição automática do vídeo. "
                "Verifique se as legendas automáticas estão disponíveis.")
    
    prompt = (f"""
    Por favor, faça um resumo conciso e informativo do seguinte conteúdo,
    mantendo os pontos principais e ideias centrais. Se o texto estiver em inglês,
    faça o resumo em português:
    
    Título: {title}
    
    Conteúdo:
    {transcript[:8000]}
    
    Instruções:
    - Identifique e mantenha os pontos principais
    - Organize o conteúdo de forma lógica e coesa
    - Explique termos técnicos de forma simples
    - Mantenha um tom profissional e acessível
    - Corrija possíveis erros da transcrição automática
    """)
    
    response = model.generate_content(prompt)
    return response.text

# Exemplo de uso:
if __name__ == "__main__":
    API_KEY = "sua_api_key_aqui"
    video_url = "https://www.youtube.com/watch?v=video_id"
    
    summary = summarize_video(video_url, API_KEY)
    print(summary)
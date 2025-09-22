const API_BASE = localStorage.getItem('THOMAS_API') || 'http://localhost:8000';

const micBtn = document.getElementById('micBtn');
const sendBtn = document.getElementById('sendBtn');
const textInput = document.getElementById('textInput');
const responseDiv = document.getElementById('response');
const newsDiv = document.getElementById('news');
const hero = document.getElementById('hero');
const fsBtn = document.getElementById('fsBtn');
const splineEl = document.getElementById('spline');
let isRecognizing = false;

function speak(text){
  try{
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = 'en-US';
    speechSynthesis.speak(utter);
  }catch(e){
    console.warn('Speech synthesis not available', e);
  }
}

async function callBackend(command){
  const r = await fetch(`${API_BASE}/process`,{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({command})
  });
  if(!r.ok){
    throw new Error(`Request failed: ${r.status}`);
  }
  return r.json();
}

function handleAction(res){
  responseDiv.textContent = res.message || '';
  newsDiv.innerHTML = '';
  switch(res.action){
    case 'speak':
    case 'ai_reply':
      speak(res.message);
      break;
    case 'open_url':
      speak(res.message);
      if(res.data && res.data.url){
        window.open(res.data.url, '_blank');
      }
      break;
    case 'play_song':
      speak(res.message);
      if(res.data && res.data.url){
        window.open(res.data.url, '_blank');
      }
      break;
    case 'news':
      speak('Here are the latest headlines.');
      if(res.data && Array.isArray(res.data.titles)){
        const ul = document.createElement('ul');
        res.data.titles.forEach(t => {
          const li = document.createElement('li');
          li.textContent = t;
          ul.appendChild(li);
        });
        newsDiv.appendChild(ul);
      }
      break;
    default:
      break;
  }
}

async function sendCommand(cmd){
  if(!cmd) return;
  sendBtn.disabled = true; micBtn.disabled = true;
  try{
    const res = await callBackend(cmd);
    handleAction(res);
  }catch(e){
    responseDiv.textContent = `Error: ${e.message}`;
  }finally{
    sendBtn.disabled = false; micBtn.disabled = false;
  }
}

sendBtn.addEventListener('click', ()=>{
  const cmd = textInput.value.trim();
  sendCommand(cmd);
});

textInput.addEventListener('keydown', (e)=>{
  if(e.key === 'Enter'){
    sendCommand(textInput.value.trim());
  }
});

// Mic button using Web Speech API
micBtn.addEventListener('click', ()=>{
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if(!SpeechRecognition){
    responseDiv.textContent = 'Mic error: Speech recognition is not supported in this browser. Use Chrome/Edge.';
    return;
  }
  // Request mic permission first to avoid silent failures on some browsers
  navigator.mediaDevices.getUserMedia({audio:true}).then(stream=>{
    // Immediately stop tracks; we only needed permission prompt
    stream.getTracks().forEach(t=>t.stop());

    const recog = new SpeechRecognition();
    recog.lang = 'en-US';
    recog.interimResults = false;
    recog.maxAlternatives = 1;

    recog.onstart = ()=>{
      isRecognizing = true;
      micBtn.disabled = true;
      responseDiv.textContent = 'Listening...';
      hero && hero.classList.add('speaking');
    };
    recog.onresult = (evt)=>{
      const transcript = evt.results[0][0].transcript;
      textInput.value = transcript;
      sendCommand(transcript);
    };
    recog.onerror = (evt)=>{
      responseDiv.textContent = `Mic error: ${evt.error}`;
    };
    recog.onend = ()=>{
      isRecognizing = false;
      micBtn.disabled = false;
      hero && hero.classList.remove('speaking');
      if(!responseDiv.textContent){
        responseDiv.textContent = 'No speech detected.';
      }
    };
    try{
      recog.start();
    }catch(e){
      responseDiv.textContent = `Mic start failed: ${e.message}`;
      micBtn.disabled = false;
    }
  }).catch(err=>{
    responseDiv.textContent = `Mic permission denied or unavailable: ${err.message}`;
  });
});

// Fullscreen toggle for Spline canvas
fsBtn?.addEventListener('click', async ()=>{
  const el = hero;
  if(!el) return;
  try{
    if(!document.fullscreenElement){
      await el.requestFullscreen();
    }else{
      await document.exitFullscreen();
    }
  }catch(e){
    responseDiv.textContent = `Fullscreen error: ${e.message}`;
  }
});

// Removed Spline URL persistence controls as requested

// Prevent zooming inside Spline viewer to keep a consistent size
if(splineEl){
  const prevent = (e)=>{
    e.preventDefault();
  };
  splineEl.addEventListener('wheel', prevent, {passive:false});
  splineEl.addEventListener('gesturestart', prevent);
  splineEl.addEventListener('gesturechange', prevent);
  splineEl.addEventListener('gestureend', prevent);
  // Trackpad pinch on some browsers
  document.addEventListener('wheel', (e)=>{
    if (e.ctrlKey) e.preventDefault();
  }, {passive:false});
}



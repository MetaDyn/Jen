const pulseBtn = document.getElementById('pulseBtn');
const themeBtn = document.getElementById('themeBtn');
const statusBadge = document.getElementById('statusBadge');
const consoleEl = document.querySelector('.console');

function log(message) {
  const line = document.createElement('div');
  line.className = 'console-line';
  line.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
  consoleEl.prepend(line);
}

pulseBtn.addEventListener('click', () => {
  document.body.classList.add('pulse');
  statusBadge.textContent = 'Pulsing';
  log('Pulse animation triggered.');
  window.setTimeout(() => {
    document.body.classList.remove('pulse');
    statusBadge.textContent = 'Idle';
  }, 700);
});

themeBtn.addEventListener('click', () => {
  document.body.classList.toggle('light');
  const light = document.body.classList.contains('light');
  statusBadge.textContent = light ? 'Light Theme' : 'Dark Theme';
  log(`Theme toggled to ${light ? 'light' : 'dark'} mode.`);
});

log('Canvas demo ready. Static hosting compatible.');

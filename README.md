# stockrecommener

### cloning code and running dependencies
<pre>
  git clone https://github.com/pankajr141/stockrecommener.git
  cd stockrecommener
  sh startup.sh
</pre>

### Running UI application
<pre>
  cd stockrecommener
  streamlit run main.py &> logs.txt &
  nohup localtunnel --port 8501

  tail nohup.out   -- Get URI and open that in browser
  tail logs.txt    -- Get IP as password
</pre>

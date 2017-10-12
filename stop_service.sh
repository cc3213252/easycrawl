supervisorctl -c $HOME/supervisor/supervisord.conf stop easycrawl:
cp ./supervisor/supervisor.ini $HOME/supervisor/supervisord.conf.d/easycrawl.conf
supervisorctl -c $HOME/supervisor/supervisord.conf add easycrawl
supervisorctl -c $HOME/supervisor/supervisord.conf update easycrawl
true

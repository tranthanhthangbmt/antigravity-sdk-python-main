import React, { useEffect, useRef } from 'react';

function TerminalLog({ logs }) {
  const endRef = useRef(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [logs]);

  return (
    <div className="terminal-container">
      <div className="terminal-header">
        <div className="mac-btn close"></div>
        <div className="mac-btn min"></div>
        <div className="mac-btn max"></div>
      </div>
      <div className="terminal-body">
        {logs.map((log, i) => (
          <div key={i} className="log-line">
            <span className="log-time">[{log.time}]</span>
            <span className={log.text.includes('[Agent Thought]') ? 'log-agent' : ''}>
              {log.text}
            </span>
          </div>
        ))}
        {logs.length === 0 && <div>Waiting for agent connection...</div>}
        <div ref={endRef} />
      </div>
    </div>
  );
}

export default TerminalLog;

import React from 'react';

function DetailedProgress({ parts }) {
  
  const getIcon = (status) => {
    switch(status) {
      case 'extracting': return '⏳';
      case 'translating': return '⚙️';
      case 'completed': return '✓';
      default: return '•';
    }
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(140px, 1fr))', gap: '0.5rem' }}>
      {parts.map(part => {
        const isActive = part.status === 'extracting' || part.status === 'translating';
        let bgColor = 'rgba(255,255,255,0.05)';
        let textColor = 'var(--text-color)';
        let borderColor = 'transparent';
        
        if (part.status === 'completed') {
          bgColor = 'rgba(16, 185, 129, 0.1)';
          textColor = '#4ade80';
        } else if (isActive) {
          bgColor = 'rgba(59, 130, 246, 0.1)';
          textColor = '#60a5fa';
          borderColor = 'rgba(59, 130, 246, 0.5)';
        }

        return (
          <div 
            key={part.id} 
            style={{
              padding: '0.75rem',
              borderRadius: '0.5rem',
              background: bgColor,
              color: textColor,
              border: `1px solid ${borderColor}`,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: '0.25rem',
              transition: 'all 0.3s ease'
            }}
          >
            <div style={{ fontSize: '1.25rem' }}>
              {getIcon(part.status)}
            </div>
            <div style={{ fontSize: '0.75rem', fontWeight: 'bold', textAlign: 'center' }}>
              {part.name.split(':')[0]} {/* Chỉ lấy chữ Phần 1, Phần 2 cho gọn */}
            </div>
            <div style={{ fontSize: '0.65rem', opacity: 0.8, textTransform: 'capitalize' }}>
              {part.status}
            </div>
          </div>
        );
      })}
    </div>
  );
}

export default DetailedProgress;

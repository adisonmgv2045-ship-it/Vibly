import { useState, useEffect } from 'react';
import './index.css';

// Componente de Login
const LoginScreen = ({ onLogin }) => {
  const [step, setStep] = useState(1); // 1: Phone, 2: Code
  const [phone, setPhone] = useState("");
  const [email, setEmail] = useState("");
  const [countryCode, setCountryCode] = useState("+53");
  const [code, setCode] = useState("");

  const getFlag = (code) => {
    const flags = {
      "+1": "🇺🇸", "+52": "🇲🇽", "+34": "🇪🇸", "+53": "🇨🇺", "+57": "🇨🇴", 
      "+54": "🇦🇷", "+56": "🇨🇱", "+58": "🇻🇪", "+51": "🇵🇪", "+55": "🇧🇷",
      "+44": "🇬🇧", "+33": "🇫🇷", "+49": "🇩🇪", "+39": "🇮🇹", "+7": "🇷🇺",
      "+86": "🇨🇳", "+81": "🇯🇵", "+91": "🇮🇳", "+507": "🇵🇦", "+506": "🇨🇷",
      "+503": "🇸🇻", "+502": "🇬🇹", "+504": "🇭🇳", "+591": "🇧🇴", "+593": "🇪🇨",
      "+595": "🇵🇾", "+598": "🇺🇾"
    };
    return flags[code] || "🌍";
  };

  const handleSendCode = () => {
    if (!phone || !email) {
        alert("Por favor ingresa teléfono y correo");
        return;
    }
    const fullPhone = `${countryCode}${phone}`;
    fetch('http://localhost:8000/auth/send-code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone_number: fullPhone, email: email })
    })
    .then(res => {
        if (!res.ok) throw new Error(`Error ${res.status}: ${res.statusText}`);
        return res.json();
    })
    .then(() => setStep(2))
    .catch(err => {
        console.error("Login error:", err);
        alert("Error enviando código: " + err.message);
    });
  };

  const handleVerify = () => {
    const fullPhone = `${countryCode}${phone}`;
    fetch('http://localhost:8000/auth/verify-code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone_number: fullPhone, email: email, code: code })
    })
    .then(res => {
        if (!res.ok) throw new Error("Código inválido");
        return res.json();
    })
    .then(data => {
      onLogin(data.user);
    })
    .catch(err => {
        console.error("Verify error:", err);
        alert(err.message);
    });
  };

  return (
    <div className="login-container" style={{display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', background: 'var(--bg-light)'}}>
      <h1 style={{fontSize: '3rem', marginBottom: '40px', background: 'var(--primary-gradient)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent'}}>Vibly</h1>
      
      <div style={{background: 'white', padding: '30px', borderRadius: '20px', boxShadow: '0 10px 25px rgba(0,0,0,0.1)', width: '100%', maxWidth: '400px'}}>
        {step === 1 ? (
          <>
            <h2 style={{marginBottom: '20px'}}>Ingresa tus datos</h2>
            <div style={{display: 'flex', gap: '10px', marginBottom: '15px'}}>
              <div style={{display: 'flex', alignItems: 'center', background: 'white', border: '1px solid #ddd', borderRadius: '10px', padding: '0 10px', width: '110px'}}>
                <span style={{fontSize: '1.5rem', marginRight: '5px'}}>{getFlag(countryCode)}</span>
                <input 
                  type="text" 
                  value={countryCode} 
                  onChange={e => setCountryCode(e.target.value)}
                  style={{border: 'none', outline: 'none', width: '100%', fontSize: '1rem', fontWeight: 'bold'}}
                />
              </div>
              <input 
                type="tel" 
                placeholder="Número" 
                value={phone}
                onChange={e => setPhone(e.target.value)}
                style={{flex: 1, padding: '10px', borderRadius: '10px', border: '1px solid #ddd'}}
              />
            </div>
            <div style={{marginBottom: '20px'}}>
                <input 
                    type="email" 
                    placeholder="Correo electrónico (Gmail)" 
                    value={email}
                    onChange={e => setEmail(e.target.value)}
                    style={{width: '100%', padding: '10px', borderRadius: '10px', border: '1px solid #ddd'}}
                />
            </div>
            <button onClick={handleSendCode} style={{width: '100%', padding: '12px', background: 'var(--primary-color)', color: 'white', border: 'none', borderRadius: '10px', cursor: 'pointer', fontWeight: 'bold'}}>
              Enviar Código por Correo
            </button>
          </>
        ) : (
          <>
            <h2 style={{marginBottom: '20px'}}>Verificar Código</h2>
            <p style={{marginBottom: '20px', color: '#666'}}>Enviado a {email}</p>
            <input 
              type="text" 
              placeholder="Código de 6 dígitos" 
              value={code}
              onChange={e => setCode(e.target.value)}
              style={{width: '100%', padding: '10px', borderRadius: '10px', border: '1px solid #ddd', marginBottom: '20px', textAlign: 'center', letterSpacing: '5px', fontSize: '1.2rem'}}

            />
            <button onClick={handleVerify} style={{width: '100%', padding: '12px', background: 'var(--primary-color)', color: 'white', border: 'none', borderRadius: '10px', cursor: 'pointer', fontWeight: 'bold'}}>
              Verificar y Entrar
            </button>
            <button onClick={() => setStep(1)} style={{width: '100%', marginTop: '10px', background: 'transparent', color: '#666', border: 'none', cursor: 'pointer'}}>
              Volver
            </button>
          </>
        )}
      </div>
    </div>
  );
};

const ChatProfileDetails = ({ chatId, isGroup, currentUserId, onContactUpdate }) => {
    const [details, setDetails] = useState(null);
    const [loading, setLoading] = useState(true);
    const [alias, setAlias] = useState("");

    useEffect(() => {
        fetch(`http://localhost:8000/chats/${chatId}/details?user_id=${currentUserId}`)
            .then(res => {
                if(res.ok) return res.json();
                throw new Error("Failed to fetch");
            })
            .then(data => {
                setDetails(data);
                setLoading(false);
            })
            .catch(err => {
                console.error(err);
                setLoading(false);
            });

    }, [chatId, currentUserId]);

    const handleSaveContact = () => {
        if (!details?.other_user) return;
        
        fetch(`http://localhost:8000/contacts/?user_id=${currentUserId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                contact_user_id: details.other_user.id,
                alias: alias || details.other_user.full_name || "Contacto"
            })
        })
        .then(res => res.json())
        .then(contact => {
            alert("Contacto guardado!");
            if (onContactUpdate) onContactUpdate(contact);
        })
        .catch(err => console.error("Error saving contact:", err));
    };

    if (loading) return <p>Cargando...</p>;
    if (!details) return <p>No se pudo cargar la información.</p>;

    if (isGroup) {
        return (
             <div style={{textAlign: 'left', padding: '10px', background: '#f5f5f5', borderRadius: '10px'}}>
                <p><strong>Grupo</strong></p>
                <p>{details.members.length} miembros</p>
                <div style={{marginTop: '10px', maxHeight: '150px', overflowY: 'auto'}}>
                    {details.members.map(m => (
                        <div key={m.id} style={{display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '5px'}}>
                            <img src={m.avatar_url || "https://i.pravatar.cc/150?u=0"} style={{width: '30px', height: '30px', borderRadius: '50%'}} />
                            <span>{m.full_name || m.phone_number}</span>
                        </div>
                    ))}
                </div>
            </div>
        )
    }
    
    return (
        <div style={{textAlign: 'left', padding: '15px', background: '#f5f5f5', borderRadius: '10px'}}>
            <p><strong>Bio:</strong></p>
            <p style={{fontStyle: 'italic', color: '#555', marginBottom: '15px'}}>{details.other_user?.bio || "Sin descripción."}</p>
            
            <div style={{display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '20px'}}>
                <div>
                    <span style={{fontSize: '0.8rem', color: '#888'}}>Teléfono</span>
                    <p>{details.other_user?.phone_number}</p>
                </div>
                <div>
                    <span style={{fontSize: '0.8rem', color: '#888'}}>Nombre de usuario</span>
                    <p>@{details.other_user?.username || "No establecido"}</p>
                </div>
                 <div>
                    <span style={{fontSize: '0.8rem', color: '#888'}}>Nombre</span>
                    <p>{details.other_user?.full_name || "No establecido"}</p>
                </div>
            </div>

            <div style={{borderTop: '1px solid #ddd', paddingTop: '15px'}}>
                <label style={{display: 'block', marginBottom: '5px', fontWeight: 'bold'}}>Guardar como contacto</label>
                <div style={{display: 'flex', gap: '10px'}}>
                    <input 
                        type="text" 
                        placeholder="Nombre del contacto" 
                        value={alias}
                        onChange={e => setAlias(e.target.value)}
                        style={{flex: 1, padding: '8px', borderRadius: '5px', border: '1px solid #ddd'}}
                    />
                    <button onClick={handleSaveContact} style={{padding: '8px 15px', background: 'var(--primary-color)', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer'}}>
                        Guardar
                    </button>
                </div>
            </div>
        </div>
    );
};

function App() {
  const [user, setUser] = useState(null);
  const [darkMode, setDarkMode] = useState(false);
  const [activeTab, setActiveTab] = useState('chats'); // 'chats', 'feed', 'reels', 'settings'
  const [selectedChat, setSelectedChat] = useState(null);
  const [chats, setChats] = useState([]);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const [reels, setReels] = useState([]);
  const [editName, setEditName] = useState("");
  const [editUsername, setEditUsername] = useState("");
  const [showNewChatModal, setShowNewChatModal] = useState(false);
  const [searchPhone, setSearchPhone] = useState("");
  const [foundUser, setFoundUser] = useState(null);
  const [showChatProfile, setShowChatProfile] = useState(false);
  const [editBio, setEditBio] = useState("");
  const [contacts, setContacts] = useState([]);

  // Cargar usuario de localStorage al iniciar
  useEffect(() => {
    const savedUser = localStorage.getItem('vibly_user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    localStorage.setItem('vibly_user', JSON.stringify(userData));
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('vibly_user');
    setSelectedChat(null);
    setChats([]);
  };

  const fetchChats = () => {
    if (!user || !user.id) return;
    fetch(`http://localhost:8000/chats?user_id=${user.id}`)
      .then(res => {
        if (!res.ok) throw new Error("Failed to fetch chats");
        return res.json();
      })
      .then(data => {
        if (Array.isArray(data)) {
          setChats(data);
        } else {
          console.error("Chats data is not an array:", data);
          setChats([]);
        }
      })
      .catch(err => console.error("Error fetching chats:", err));
  };

  // Simular carga de datos del backend
  useEffect(() => {
    fetchChats();
      
    // Cargar Reels si estamos en esa tab
    if (activeTab === 'reels') {
       fetch('http://localhost:8000/reels')
        .then(res => res.json())
        .then(data => setReels(data))
        .catch(err => console.error("Error fetching reels:", err));
    }
  }, [activeTab, user]);

  // Cargar mensajes cuando se selecciona un chat
  useEffect(() => {
    if (selectedChat) {
      fetch(`http://localhost:8000/chats/${selectedChat.id}/messages`)
        .then(res => res.json())
        .then(data => setMessages(data))
        .catch(err => console.error("Error fetching messages:", err));
    }
  }, [selectedChat]);

  useEffect(() => {
      if (user) {
          setEditName(user.full_name || "");
          setEditUsername(user.username || "");
          setEditBio(user.bio || "");
      }
  }, [user]);

  useEffect(() => {
      if (user && user.id) {
          fetch(`http://localhost:8000/contacts/?user_id=${user.id}`)
            .then(res => {
                if (!res.ok) throw new Error("Failed to fetch contacts");
                return res.json();
            })
            .then(data => {
                if (Array.isArray(data)) {
                    setContacts(data);
                } else {
                    setContacts([]);
                }
            })
            .catch(err => console.error("Error fetching contacts:", err));
      }
  }, [user]);

  const toggleTheme = () => {
    setDarkMode(!darkMode);
  };

  const sendMessage = () => {
    if (!newMessage.trim() || !selectedChat) return;

    const messageData = {
      content: newMessage,
      chat_id: selectedChat.id,
      sender_id: user.id
    };

    fetch('http://localhost:8000/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(messageData),
    })
      .then(res => res.json())
      .then(savedMessage => {
        setMessages([...messages, savedMessage]);
        setNewMessage("");
      })
      .catch(err => console.error("Error sending message:", err));
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  const handleUpdateProfile = () => {
      fetch(`http://localhost:8000/users/${user.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ full_name: editName, username: editUsername, bio: editBio })
      })
      .then(res => res.json())
      .then(updatedUser => {
          setUser(updatedUser);
          alert("Perfil actualizado!");
      })
      .catch(err => console.error("Error updating profile:", err));
  };

  const handleAvatarUpload = (e) => {
      const file = e.target.files[0];
      if (!file) return;

      const formData = new FormData();
      formData.append("file", file);

      fetch(`http://localhost:8000/users/${user.id}/avatar`, {
          method: 'POST',
          body: formData
      })
      .then(res => res.json())
      .then(data => {
          setUser({ ...user, avatar_url: data.avatar_url });
      })
      .catch(err => console.error("Error uploading avatar:", err));
  };

  const handleSearchUser = () => {
      fetch(`http://localhost:8000/users/search/?phone=${encodeURIComponent(searchPhone)}`)
      .then(res => {
          if (!res.ok) throw new Error("Usuario no encontrado");
          return res.json();
      })
      .then(data => setFoundUser(data))
      .catch(err => {
          setFoundUser(null);
          alert(err.message);
      });
  };

  const handleStartChat = () => {
      if (!foundUser || !user) return;

      fetch('http://localhost:8000/chats/private', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
              target_user_id: foundUser.id,
              current_user_id: user.id
          })
      })
      .then(res => res.json())
      .then(chat => {
          // Add to chats list if not present (simplified)
          if (!chats.find(c => c.id === chat.id)) {
              setChats([chat, ...chats]);
          }
          setSelectedChat(chat);
          setShowNewChatModal(false);
          setFoundUser(null);
          setSearchPhone("");
      })
      .catch(err => console.error("Error creating chat:", err));
  };

  const getDisplayName = (targetUser) => {
      if (!targetUser) return "Usuario";
      const contact = contacts.find(c => String(c.contact_user_id) === String(targetUser.id));
      return contact ? contact.alias : (targetUser.full_name || targetUser.phone_number);
  };

  if (!user) {
    return <LoginScreen onLogin={handleLogin} />;
  }

  return (
    <div className={`app-container ${darkMode ? 'dark' : 'light'} ${selectedChat ? 'chat-active' : ''}`}>
      
      {/* Sidebar */}
      <div className="sidebar">
        <div className="sidebar-header">
          <div className="profile-pic" onClick={() => setActiveTab('settings')} title="Configuración">
             <img src={user.avatar_url || "https://i.pravatar.cc/150?u=0"} alt="Me" style={{width: '100%', height: '100%', borderRadius: '50%'}} />
          </div>
          <div className="header-icons">
            <span title="Estados">⭕</span> 
            <span title="Nuevo Grupo">👥</span>
            <span title="Nuevo Chat" onClick={() => setShowNewChatModal(true)}>💬</span>
            <span onClick={handleLogout} title="Cerrar Sesión">🚪</span>
          </div>
        </div>

        <div className="nav-tabs">
          <div className={`nav-tab ${activeTab === 'chats' ? 'active' : ''}`} onClick={() => setActiveTab('chats')}>Chats</div>
          <div className={`nav-tab ${activeTab === 'reels' ? 'active' : ''}`} onClick={() => setActiveTab('reels')}>Reels</div>
          <div className={`nav-tab ${activeTab === 'feed' ? 'active' : ''}`} onClick={() => setActiveTab('feed')}>Feed</div>
        </div>

        {activeTab === 'chats' && (
          <>
            <div className="search-bar">
              <span>🔍</span>
              <input type="text" placeholder="Buscar o iniciar nuevo chat" />
            </div>

            <div className="chat-list">
              {chats.map(chat => {
                  // Try to find if this chat corresponds to a contact
                  // This is imperfect because we don't have the other user ID in the chat object in the list
                  // But if the chat name is a phone number, we can try to match it?
                  // Or better, we should update the backend to return the other user ID for private chats.
                  // For now, let's just display chat.name. 
                  // If we want to support aliases in the list, we need the backend change.
                  // Let's assume for now the user sees what the backend sends.
                  return (
                <div 
                  key={chat.id} 
                  className="chat-item"
                  onClick={() => setSelectedChat(chat)}
                  style={{ backgroundColor: selectedChat?.id === chat.id ? (darkMode ? '#2a3942' : '#f0f2f5') : 'transparent' }}
                >
                  <img src={chat.avatar_url || chat.avatar} alt={chat.name} />
                  <div className="chat-info">
                    <div className="chat-header">
                      <span className="chat-name">{chat.name}</span>
                      <span className="chat-time">{chat.updated_at ? new Date(chat.updated_at).toLocaleDateString() : chat.time}</span>
                    </div>
                    <div className="chat-last-msg">
                      {chat.last_message}
                    </div>
                  </div>
                </div>
              )})}
            </div>
          </>
        )}
        
        {activeTab === 'reels' && (
           <div className="reels-list" style={{padding: '10px', overflowY: 'auto', height: 'calc(100vh - 150px)'}}>
              <h3 style={{marginBottom: '10px'}}>Reels Cortos</h3>
              {reels.length === 0 && <p>No hay reels aún.</p>}
              {reels.map(reel => (
                <div key={reel.id} style={{marginBottom: '20px', borderRadius: '10px', overflow: 'hidden', position: 'relative'}}>
                   <div style={{height: '300px', background: '#000', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white'}}>
                      VIDEO PLACEHOLDER
                   </div>
                   <div style={{padding: '10px', background: darkMode ? '#2d2d2d' : 'white'}}>
                      <p style={{fontWeight: 'bold'}}>{reel.caption}</p>
                      <p style={{fontSize: '0.8rem', color: '#888'}}>❤️ {reel.likes} likes</p>
                   </div>
                </div>
              ))}
           </div>
        )}

        {activeTab === 'settings' && (
          <div style={{padding: '20px'}}>
            <h2>Configuración</h2>
            
            <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', marginBottom: '20px', padding: '20px', background: darkMode ? '#2d2d2d' : 'white', borderRadius: '10px'}}>
                <div style={{position: 'relative', width: '100px', height: '100px', marginBottom: '20px'}}>
                    <img src={user.avatar_url || "https://i.pravatar.cc/150?u=0"} alt="Profile" style={{width: '100%', height: '100%', borderRadius: '50%', objectFit: 'cover'}} />
                    <label htmlFor="avatar-upload" style={{position: 'absolute', bottom: '0', right: '0', background: 'var(--primary-color)', color: 'white', borderRadius: '50%', width: '30px', height: '30px', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer', boxShadow: '0 2px 5px rgba(0,0,0,0.2)'}}>
                        📷
                    </label>
                    <input id="avatar-upload" type="file" accept="image/*" onChange={handleAvatarUpload} style={{display: 'none'}} />
                </div>
                
                <div style={{width: '100%', marginBottom: '15px'}}>
                    <label style={{display: 'block', marginBottom: '5px', fontWeight: 'bold'}}>Nombre Completo</label>
                    <input 
                        type="text" 
                        value={editName} 
                        onChange={e => setEditName(e.target.value)}
                        style={{width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #ddd', background: darkMode ? '#404040' : 'white', color: darkMode ? 'white' : 'black'}}
                    />
                </div>

                <div style={{width: '100%', marginBottom: '20px'}}>
                    <label style={{display: 'block', marginBottom: '5px', fontWeight: 'bold'}}>Usuario (@)</label>
                    <input 
                        type="text" 
                        value={editUsername} 
                        onChange={e => setEditUsername(e.target.value)}
                        style={{width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #ddd', background: darkMode ? '#404040' : 'white', color: darkMode ? 'white' : 'black'}}
                    />
                </div>

                <div style={{width: '100%', marginBottom: '20px'}}>
                    <label style={{display: 'block', marginBottom: '5px', fontWeight: 'bold'}}>Descripción (Bio)</label>
                    <textarea 
                        value={editBio} 
                        onChange={e => setEditBio(e.target.value)}
                        style={{width: '100%', padding: '10px', borderRadius: '5px', border: '1px solid #ddd', background: darkMode ? '#404040' : 'white', color: darkMode ? 'white' : 'black', minHeight: '80px'}}
                    />
                </div>

                <button onClick={handleUpdateProfile} style={{width: '100%', padding: '12px', background: 'var(--primary-color)', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer', fontWeight: 'bold'}}>
                    Guardar Cambios
                </button>
            </div>

            <div style={{marginTop: '20px'}}>
               <div style={{padding: '15px', borderBottom: '1px solid #ddd'}}>
                 <h4>Privacidad</h4>
                 <p>Quién puede ver mi última vez</p>
               </div>
               <div style={{padding: '15px', borderBottom: '1px solid #ddd'}}>
                 <h4>Notificaciones</h4>
                 <p>Tonos y vibración</p>
               </div>
               <button onClick={() => setUser(null)} style={{marginTop: '20px', width: '100%', padding: '10px', background: '#ff4444', color: 'white', border: 'none', borderRadius: '5px'}}>
                 Cerrar Sesión
               </button>
            </div>
          </div>
        )}
      </div>

      {/* Main Chat Area */}
      <div className="main-chat">
        {selectedChat ? (
          <>
            <div className="chat-top-bar">
              <button className="back-btn" onClick={() => setSelectedChat(null)}>←</button>
              <div style={{display: 'flex', alignItems: 'center', gap: '15px', cursor: 'pointer'}} onClick={() => setShowChatProfile(true)}>
                <img src={selectedChat.avatar_url || selectedChat.avatar} alt="" style={{width: '40px', height: '40px', borderRadius: '50%'}} />
                <span style={{fontWeight: '600', fontSize: '1.1rem'}}>
                    {/* Use contact alias if available for private chats */}
                    {!selectedChat.is_group ? (
                        // We need to find the other user ID to check contacts. 
                        // Since we don't have it easily in 'selectedChat' object without fetching details,
                        // we can try to match by name if it was set to phone number, or just rely on the fact that
                        // we should probably update 'selectedChat' name when loading chats if we have contacts.
                        // BUT, for now, let's just use the name from the chat object which we might need to update 
                        // or we can try to find a contact that matches the chat name (if it's a phone number).
                        // A better way is to update the chat list rendering to use getDisplayName.
                        selectedChat.name 
                    ) : selectedChat.name}
                </span>
              </div>
              <div className="header-icons">
                <span>🔍</span>
                <span>⋮</span>
              </div>
            </div>

            <div className="messages-area">
              {messages.map((msg) => (
                <div key={msg.id} className={`message ${String(msg.sender_id) === String(user.id) ? 'sent' : 'received'}`}>
                  {msg.content}
                  <div className="message-time">{new Date(msg.timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
                </div>
              ))}
            </div>

            <div className="chat-input-area">
              <button className="icon-btn">😊</button>
              <button className="icon-btn">📎</button>
              <input 
                type="text" 
                placeholder="Escribe un mensaje" 
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                onKeyPress={handleKeyPress}
              />
              <button className="icon-btn" onClick={sendMessage}>➤</button>
            </div>
          </>
        ) : (
          <div style={{display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', color: '#888'}}>
            <h1 style={{fontSize: '3rem', marginBottom: '20px', background: 'var(--primary-gradient)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent'}}>Vibly</h1>
            <p>Selecciona un chat para comenzar a hablar</p>
            <p>o explora los Reels y el Feed.</p>
          </div>
        )}
      </div>

      {/* New Chat Modal */}
      {showNewChatModal && (
        <div className="modal-overlay" onClick={() => setShowNewChatModal(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <h2>Nuevo Chat</h2>
            <div className="search-user">
              <input 
                type="text" 
                placeholder="Buscar por número de teléfono" 
                value={searchPhone}
                onChange={e => setSearchPhone(e.target.value)}
              />
              <button onClick={handleSearchUser}>Buscar</button>
            </div>
            {foundUser && (
              <div className="found-user" onClick={handleStartChat}>
                <img src={foundUser.avatar_url || "https://i.pravatar.cc/150?u=0"} alt="Usuario encontrado" />
                <div className="user-info">
                  <span className="user-name">{foundUser.full_name}</span>
                  <span className="user-phone">{foundUser.phone_number}</span>
                </div>
              </div>
            )}
            {!foundUser && searchPhone && (
              <div className="no-user-found">
                <p>No se encontró ningún usuario con ese número.</p>
              </div>
            )}
            <button className="close-modal" onClick={() => setShowNewChatModal(false)}>✖️</button>
          </div>
        </div>
      )}

      {/* Chat Profile Modal */}
      {showChatProfile && selectedChat && (
        <div className="modal-overlay" onClick={() => setShowChatProfile(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()} style={{textAlign: 'center'}}>
            <img src={selectedChat.avatar_url || selectedChat.avatar} alt="" style={{width: '100px', height: '100px', borderRadius: '50%', marginBottom: '15px', objectFit: 'cover'}} />
            <h2 style={{marginBottom: '5px'}}>{selectedChat.name}</h2>
            {/* We need to fetch user details if it's a private chat to get the bio, or store it in chat object. 
                For now, let's assume we might need to fetch it or it's not available yet. 
                Ideally, we should fetch the user profile when opening this modal.
            */}
            <p style={{color: '#666', marginBottom: '20px'}}>
                {/* Placeholder for bio or phone number */}
                {selectedChat.is_group ? "Grupo" : (selectedChat.name !== "Usuario" ? "Usuario de Vibly" : "")}
            </p>
            
            {/* Fetch and display bio logic would go here. For simplicity, let's just show a placeholder or fetch it on mount of this modal */}
            <ChatProfileDetails 
                chatId={selectedChat.id} 
                isGroup={selectedChat.is_group} 
                currentUserId={user.id} 
                onContactUpdate={(newContact) => {
                    // Update contacts list
                    const existing = contacts.find(c => c.id === newContact.id);
                    if (existing) {
                        setContacts(contacts.map(c => c.id === newContact.id ? newContact : c));
                    } else {
                        setContacts([...contacts, newContact]);
                    }
                    // Refresh chats to update the name in the list
                    fetchChats();
                    // Also update selectedChat name immediately
                    setSelectedChat(prev => ({...prev, name: newContact.alias}));
                }}
            />

            <button className="close-modal" onClick={() => setShowChatProfile(false)}>✖️</button>
          </div>
        </div>
      )}

      {/* Floating Action Button */}
      <div className="fab" title="Nuevo Chat" onClick={() => setShowNewChatModal(true)}>
        +
      </div>

    </div>
  );
}

export default App;


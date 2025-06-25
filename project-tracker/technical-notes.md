# AutoGPT Project - Technical Notes & Reference

## 🖥️ **Environment Configuration**

### **System Specifications**
- **OS**: Windows 10.0.22631
- **Shell**: PowerShell 
- **Node.js**: v22.11.0
- **npm**: v10.9.0
- **Docker**: Desktop with WSL2 backend
- **WSL2 Kernel**: 6.6.87.2-microsoft-standard-WSL2

### **Repository Structure**
```
C:\Fra_Asus_til_MSI\VSCode\AutoGPT\
├── autogpt_platform/          # Modern GUI-based platform
│   ├── backend/               # Python/FastAPI backend
│   ├── frontend/              # Next.js frontend
│   └── docker-compose.yml     # Service orchestration
├── classic/                   # Traditional command-line version
│   ├── forge/                 # Agent development framework
│   └── original_autogpt/      # Classic AutoGPT implementation
└── project-tracker/           # Our project management files
```

---

## ⚡ **Quick Start Commands**

### **Starting AutoGPT Platform (Windows PowerShell)**
```powershell
# Navigate to platform directory
cd C:\Fra_Asus_til_MSI\VSCode\AutoGPT\autogpt_platform

# Start backend services (27 containers)
docker compose up -d

# Start frontend (separate terminal)
cd frontend
npm install          # First time only
npm run dev         # Takes 3-5 minutes on first run

# Access points:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# Supabase Dashboard: http://localhost:8000 (user: supabase, pass: this_password_is_insecure_and_should_be_updated)
```

### **Stopping All Services**
```powershell
# Stop all Docker containers
cd C:\Fra_Asus_til_MSI\VSCode\AutoGPT\autogpt_platform
docker compose down

# Stop frontend (Ctrl+C in terminal)
```

### **Checking Service Status**
```powershell
# Check Docker containers
docker ps

# Check specific ports
netstat -an | findstr ":3000"
netstat -an | findstr ":8000"

# Check Docker info
docker info
```

---

## 🔧 **Configuration Files**

### **Backend Environment (autogpt_platform/backend/.env)**
```env
# Core API Configuration
OPENAI_API_KEY=sk-your-openai-key-here
DATABASE_URL=postgresql://postgres:password@localhost:5432/autogpt

# Database Credentials (auto-generated)
POSTGRES_PASSWORD=your-postgres-password
SUPABASE_AUTH_JWT_SECRET=your-jwt-secret

# Optional API Keys (add as needed)
ANTHROPIC_API_KEY=
GROQ_API_KEY=
REDDIT_CLIENT_ID=
DISCORD_BOT_TOKEN=
GITHUB_API_KEY=
```

### **Frontend Environment (autogpt_platform/frontend/.env.local)**
```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

---

## 🐳 **Docker Architecture**

### **Core Services (27 containers)**
```yaml
Backend Services:
- autogpt_platform-rest_server-1      # Main API server
- autogpt_platform-websocket_server-1 # Real-time communication
- autogpt_platform-executor-1         # Agent execution engine
- autogpt_platform-scheduler_server-1 # Task scheduling
- autogpt_platform-migrate-1          # Database migrations
- autogpt_platform-redis-1            # Caching layer

Supabase Services:
- supabase-db                          # PostgreSQL database
- supabase-auth                        # Authentication service
- supabase-rest                        # REST API
- supabase-realtime                    # Real-time subscriptions
- supabase-storage                     # File storage
- supabase-edge-functions              # Serverless functions
- supabase-studio                      # Database admin UI
- supabase-kong                        # API gateway
- supabase-meta                        # Metadata service
- supabase-analytics                   # Analytics service
- supabase-imgproxy                    # Image processing
- supabase-vector                      # Vector database

Infrastructure:
- rabbitmq                             # Message queue
- Networks: app-network, shared-network
```

---

## 🔍 **Troubleshooting Guide**

### **Frontend Won't Start**
**Problem**: Next.js dev server hangs or takes 5+ minutes
**Solutions**:
1. Ensure you're in the correct directory: `autogpt_platform/frontend`
2. Clear npm cache: `npm cache clean --force`
3. Delete node_modules and reinstall: `rm -rf node_modules && npm install`
4. Check if port 3000 is already in use: `netstat -an | findstr ":3000"`
5. First run always takes longer - wait 5 minutes minimum

### **Backend Services Failed**
**Problem**: Docker containers not starting
**Solutions**:
1. Ensure Docker Desktop is running
2. Check WSL2 is enabled: `wsl --status`
3. Restart Docker Desktop
4. Check port conflicts: `netstat -an | findstr ":8000"`
5. Clean Docker: `docker system prune -a`

### **Database Connection Issues**
**Problem**: Services can't connect to database
**Solutions**:
1. Check if postgres container is running: `docker ps | findstr postgres`
2. Verify database credentials in `.env` files
3. Reset database: `docker compose down -v && docker compose up -d`

### **Permission Errors (Windows)**
**Problem**: Various permission-related failures
**Solutions**:
1. Run PowerShell as Administrator
2. Enable Developer Mode in Windows Settings
3. Check WSL2 file permissions: Use Windows paths, not WSL paths

---

## 📚 **Available Automation Blocks**

### **AI & Language Models**
- OpenAI GPT models (GPT-4, GPT-3.5)
- Anthropic Claude
- Groq (fast inference)
- Text generation and analysis
- Image generation

### **Web & Data**
- HTTP requests and API calls
- Web scraping and parsing
- RSS feed monitoring
- CSV/JSON data processing
- Database operations

### **Social Media & Communication**
- Discord bot integration
- Reddit API access
- Twitter/X automation
- Medium publishing
- Email sending

### **Business Tools**
- Google Workspace integration
- GitHub repository management
- HubSpot CRM
- Linear project management
- Todoist task management

### **E-commerce & Finance**
- Apollo sales automation
- Price monitoring
- Inventory tracking
- Payment processing

---

## 🎯 **Development Best Practices**

### **Directory Navigation**
- Always use `pwd` or `Get-Location` to confirm current directory
- Use tab completion for paths
- Keep separate terminals for frontend/backend

### **Environment Variables**
- Never commit `.env` files to version control
- Use different keys for development vs production
- Document all required environment variables

### **Docker Management**
- Use `docker compose down` before shutting down
- Monitor resource usage: `docker stats`
- Clean up unused containers regularly: `docker system prune`

### **Debugging**
- Check logs: `docker compose logs service-name`
- Use browser dev tools for frontend issues
- Monitor network requests for API problems

---

## 📖 **Useful Resources**

### **Official Documentation**
- [AutoGPT Platform Docs](https://docs.agpt.co/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Supabase Documentation](https://supabase.com/docs)

### **API Documentation**
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Discord Bot API](https://discord.com/developers/docs)
- [Reddit API](https://www.reddit.com/dev/api/)

### **Learning Resources**
- Docker fundamentals
- Next.js development
- Python FastAPI
- PostgreSQL basics

---

**Last Updated**: June 25, 2025  
**Next Update**: As issues are discovered and resolved 
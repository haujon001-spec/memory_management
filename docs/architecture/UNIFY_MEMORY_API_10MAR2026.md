# Unified Memory Management API - Cross-Tool Integration

**Date Created**: March 7, 2026  
**Priority**: High  
**Goal**: Enable 3-Tier Memory System to work across Cursor, OpenClaw, and future tools via HTTP API

---

## 🎯 Objective

Transform the current Python-only memory system into a tool-agnostic architecture that serves memory queries via HTTP API, enabling:
- ✅ Cursor IDE integration (JavaScript/TypeScript client)
- ✅ OpenClaw gateway integration
- ✅ Future tool support (any HTTP-capable tool)
- ✅ Unified semantic search across all tools

---

## 📋 Tasks

### Phase 1: API Server Foundation

- [ ] **Create FastAPI Memory Server** (`memory_api_server.py`)
  - Initialize FastAPI app with CORS support
  - ConfigurationLoader for projects.json
  - Health check endpoint (`GET /health`)
  - Graceful shutdown handling
  - Port: 19000 (separate from OpenClaw 18000)

- [ ] **Implement Memory API Endpoints**
  - `GET /memory/tier` - Query specific tier (1, 2, 3a, or 3b)
  - `GET /memory/search` - Semantic search across projects
  - `POST /memory/enrich` - Get enriched context from all tiers
  - `GET /projects` - List available projects
  - `GET /projects/{project_id}/status` - Indexing status

- [ ] **Create Request/Response Models**
  - `SearchRequest` - query, project_id, n_results, tier_filter
  - `SearchResult` - document, metadata, distance, source
  - `EnrichmentRequest` - query, project_id, context_size
  - `EnrichmentResponse` - tier1, tier2, tier3a, tier3b sections
  - `HealthResponse` - status, uptime, loaded_projects, api_version

- [ ] **Add Error Handling**
  - Custom exception classes for API errors
  - 400 Bad Request for invalid parameters
  - 404 Not Found for missing projects
  - 503 Service Unavailable for ChromaDB issues
  - Structured error responses with helpful messages

---

### Phase 2: Configuration & Registry

- [ ] **Create Unified Configuration System** (`memory_config.py`)
  - Config loader from `~/.openclaw/memory_config.json`
  - Tool registry (openclaw, cursor, vscode, etc.)
  - API server settings (port, host, logging)
  - Memory paths configuration
  - Validation schema

- [ ] **Update projects.json Format**
  - Add `api_enabled` flag for each project
  - Add `indexing_interval` (default: daily)
  - Add `tier_enabled` flags for partial tiers
  - Keep backward compatibility

- [ ] **Create memory_config.json Template**
  ```json
  {
    "api_server": {
      "host": "127.0.0.1",
      "port": 19000,
      "log_level": "INFO"
    },
    "tools": [
      {"name": "cursor", "type": "editor"},
      {"name": "openclaw", "type": "gateway"},
      {"name": "vscode", "type": "editor"}
    ],
    "memory_root": "~/.openclaw",
    "semantic_cache": {
      "max_results": 10,
      "min_distance": 0.3
    }
  }
  ```

---

### Phase 3: Integration Components

- [ ] **Create Cursor Client Library** (`cursor_client.ts`)
  - HTTP client for memory API
  - Configuration manager
  - Caching layer
  - Error handling
  - TypeScript interfaces for responses

- [ ] **Create Startup Script** (`start_memory_api.py`)
  - Load configuration
  - Initialize all projects
  - Start FastAPI server
  - Setup logging
  - Handle graceful shutdown on Ctrl+C

- [ ] **Create Windows Service Script** (`register_memory_service.ps1`)
  - Register API server as Windows Service (or Task Scheduler)
  - Auto-start on system boot
  - Restart on crash
  - Log rotation

---

### Phase 4: Documentation & Examples

- [ ] **Create API Documentation** (`MEMORY_API.md`)
  - OpenAPI/Swagger specification
  - Authentication (if needed)
  - Rate limiting info
  - Example requests/responses
  - Integration guides per tool

- [ ] **Create Integration Guides**
  - Cursor integration tutorial
  - OpenClaw gateway integration
  - VS Code extension integration
  - Generic HTTP client examples

- [ ] **Create Cursor Extension Example** (`cursor_extension_example/`)
  - Sample TypeScript code
  - Configuration template
  - Build instructions

---

## 🔧 Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **API Framework** | FastAPI | Async, automatic docs, CORS built-in |
| **Port** | 19000 | Separate from OpenClaw (18000), memorable range |
| **Authentication** | None initially | Local-only (127.0.0.1), can add later |
| **Response Format** | JSON | Universal, already in use |
| **Caching** | In-memory LRU | Fast repeated queries, reasonable memory usage |
| **Logging** | Python logging | Integrated, file rotation support |

---

## 📌 Success Criteria

✅ API server starts and exposes `/health` endpoint  
✅ Can query Tier 3b (semantic search) via HTTP  
✅ Can enrich queries combining all 3 tiers  
✅ Cursor can connect and retrieve memory  
✅ OpenClaw can query memory without Python calls  
✅ API documentation is complete  
✅ Zero breaking changes to existing Python code  

---

## 🚀 Implementation Order

1. **Create API server** with basic endpoints
2. **Test with curl/Postman** before building clients
3. **Build Cursor client** and test integration
4. **Document all endpoints** with examples
5. **Create service registration** for auto-start
6. **Test full workflow**: Edit file → Index → Query from Cursor

---

## 📦 Dependencies to Add

- `fastapi` - API framework
- `uvicorn` - ASGI server
- `pydantic` - Request validation
- `python-multipart` - Form data support
- `aiofiles` - Async file I/O (optional)

---

## 🔗 Related Files

- Core: `three_tier_manager.py`, `semantic_memory.py`
- Config: `~/.openclaw/projects.json`
- Logging: `~/.openclaw/scheduler/indexer.log`

---

## 📝 Notes

- Keep API stateless for horizontal scaling (future)
- All tier queries should be cached for 5 minutes
- Semantic search timeout: 10 seconds
- Support both sync and async project loading

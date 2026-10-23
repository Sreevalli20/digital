# React UI Integration Documentation

## Overview

The Swasthya Twin application now includes a modern React-based frontend integrated with the existing Flask backend. The React UI was uploaded in the `working/` folder and has been successfully integrated with the Flask application.

## Integration Architecture

### Frontend: React + Vite + Tailwind CSS
- **Framework**: React 19 with TypeScript
- **Build Tool**: Vite 8.3
- **Styling**: Tailwind CSS 4.3
- **Icons**: Lucide React
- **Location**: `working/` directory (source), `static/` directory (built assets)

### Backend: Flask + Python
- **Framework**: Flask 3.0.3
- **Database**: SQLite
- **Python Version**: 3.12
- **Entry Point**: `app.py`

### Integration Layer
- **API Adapter**: `services/api_adapter.py` - Transforms Flask domain models to React format
- **React API Client**: `working/src/api/client.ts` - Fetches data from Flask endpoints
- **Flask Routes**: `/app` serves React SPA, `/api/react/*` provides data endpoints

## Files Changed

### New Files Created
1. `services/api_adapter.py` - Data transformation service
2. `working/` - Complete React application source code
3. `static/` - Built React static assets
4. `build.sh` - Build script for local development

### Modified Files
1. `app.py` - Added React-specific routes and API endpoints
2. `services/__init__.py` - Exported APIAdapter
3. `working/src/App.tsx` - Updated to fetch from Flask backend
4. `working/package.json` - Cleaned up dependencies

## Deployment Instructions

### Local Development

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Build React frontend:**
   ```bash
   cd working
   npm install
   npm run build
   cd ..
   cp -r working/dist static
   ```

3. **Run Flask application:**
   ```bash
   python app.py
   ```

4. **Access the application:**
   - React UI: http://localhost:5000/app
   - Original Flask UI: http://localhost:5000/
   - Health check: http://localhost:5000/health

### Alternative: Use Build Script

```bash
chmod +x build.sh
./build.sh
python app.py
```

### Render Deployment

The current `render.yaml` uses a simple Python-only build. To deploy the React UI on Render:

**Option 1: Pre-build locally and commit**
1. Build React app locally
2. Commit `static/` folder to Git
3. Push to GitHub
4. Render will deploy with existing Python build

**Option 2: Multi-stage build (requires Render Pro)**
- Update `render.yaml` to include Node.js build step
- This requires a paid Render plan with Docker support

**Current configuration** uses Option 1 for compatibility with Render Free tier.

## API Endpoints

### React-specific Endpoints

- `GET /api/react/patients` - List all patients in React format
- `GET /api/react/patients/<external_id>/observations` - Get patient observations
- `GET /api/react/patients/<external_id>/risk` - Get risk assessment
- `GET /api/react/metrics` - Get metric definitions
- `POST /api/react/demo/initialize` - Initialize demo data

### Original Flask Endpoints (Preserved)

All existing API endpoints remain unchanged:
- `GET /api/patients` - Original patient list
- `GET /api/patients/<id>` - Get patient by ID
- `POST /api/observations` - Create observation
- `POST /api/upload/csv` - CSV upload
- etc.

## Data Flow

1. **React App Loads** → Calls `/api/react/demo/initialize`
2. **Flask Backend** → Checks database, creates demo patient if needed
3. **API Adapter** → Transforms Flask Patient/Observation to React format
4. **React Client** → Receives data and displays in UI components
5. **User Interactions** → React fetches from `/api/react/*` endpoints
6. **Flask Services** → Process requests using existing business logic

## UI Components

The React UI includes the following views:
- **Overview Dashboard** - Key metrics, trends, risk summary
- **Patient Profiles** - Patient list and inspection
- **Health Trends** - Longitudinal analytics with charts
- **Risk Insights** - Rules-based risk assessment
- **Scenario Simulator** - What-if intervention simulation
- **Observations Log** - Full observation ledger
- **Data Import/Export** - CSV and evidence bundle operations
- **Evidence Reports** - Summary reports
- **Project Info** - Documentation and Flask guide

## Testing

### Backend Tests
All 50 existing tests pass:
```bash
pytest tests/ -v
```

### Manual Testing Checklist
- [ ] React UI loads at `/app`
- [ ] Demo initialization works
- [ ] Patient data displays correctly
- [ ] Observations load and display
- [ ] Risk assessment shows real data
- [ ] Navigation between views works
- [ ] Original Flask UI still works at `/`
- [ ] Health check endpoint responds

## Known Limitations

1. **Render Free Tier**: Cannot run Node.js build step in CI/CD
   - Workaround: Pre-build React locally and commit static assets
   - Future: Upgrade to Render Pro for Docker multi-stage builds

2. **Database Persistence**: SQLite on Render Free is ephemeral
   - Data resets on each deployment
   - For persistent data, use Render PostgreSQL (paid)

3. **React Mock Data**: Some components still reference mock data
   - Risk insights and scenario simulator use mock calculations
   - Future: Connect to Flask prediction/scenario engines

4. **Observation Recording**: React UI observation modal not fully connected
   - Currently displays mock functionality
   - Future: Connect to Flask observation creation endpoints

## Future Enhancements

1. Connect scenario simulator to Flask scenario engine
2. Implement real observation recording in React UI
3. Add CSV import/export in React UI
4. Connect evidence reports to Flask evidence exporter
5. Add error handling and loading states
6. Implement proper data refresh mechanisms
7. Add authentication/authorization
8. Deploy with multi-stage Docker build on Render Pro

## Rollback Instructions

If needed, to revert to the original Flask-only UI:

```bash
git checkout <commit-before-integration>
rm -rf static working services/api_adapter.py
git push origin master
```

## Support

For issues or questions:
- Check the existing Flask routes at `/` for original functionality
- React UI is served at `/app`
- Health check available at `/health`
- GitHub: https://github.com/Sreevalli20/digital

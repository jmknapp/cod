# USS Cod (SS-224) War Patrol Reports Archive

An interactive digital archive of the seven war patrol reports from USS Cod, a Gato-class submarine that served in the Pacific during World War II. This project makes these historical documents searchable and accessible, with interactive maps, glossary tooltips, and narrative summaries.

## About USS Cod

USS Cod (SS-224) was commissioned in June 1943 and completed seven war patrols in the Pacific theater between 1943 and 1945. Her combat record includes:

- **7 war patrols** across the South China Sea, Celebes Sea, and Gulf of Siam
- **12 confirmed ship sinkings** totaling approximately 27,000 tons
- **The only international submarine-to-submarine rescue in history** (HNMS O-19, July 1945)
- **3 commanding officers**: CDR James C. Dempsey (Patrols 1-3), CDR James A. Adkins (Patrols 4-6), LCDR Edwin M. Westbrook Jr. (Patrol 7)

Today, USS Cod is preserved as a **National Historic Landmark** in Cleveland, Ohio—one of the best-preserved WWII fleet submarines in existence.

## Features

### Patrol Report Viewer
- Full-text search across all seven patrol reports
- OCR-processed text with original PDF viewing
- Page-by-page navigation with synchronized text and images

### Interactive Patrol Maps
- Track USS Cod's movements across seven patrols
- Noon positions, ship contacts, aircraft contacts, and inferred positions
- Ocean depth visualization
- GeoJSON overlays for strategic areas and shipping lanes

### Glossary System
- Hover tooltips for WWII submarine terminology
- Categories: acronyms, aircraft, equipment, jargon, places
- Automatic highlighting in patrol report text

### Narrative Summaries
- Detailed summaries of each patrol with historical context
- Key events, attacks, and human interest stories
- Statistics and commanding officer information

## Technology Stack

- **Backend**: Python/Flask
- **Database**: MySQL
- **OCR**: Google Cloud Vision API
- **Maps**: Folium/Leaflet with custom GeoJSON layers
- **Frontend**: Jinja2 templates, vanilla JavaScript

## Project Structure

```
cod/
├── patrolReports/
│   ├── app.py                 # Flask application
│   ├── templates/             # HTML templates
│   │   ├── index.html         # Search interface
│   │   ├── viewer.html        # Patrol report viewer
│   │   ├── patrol_summaries.html
│   │   └── ...
│   ├── static/
│   │   ├── reports/           # PDF and OCR JSON files
│   │   ├── glossary.json      # Terminology definitions
│   │   ├── geojson/           # Map overlay data
│   │   └── aircraft_images/   # Historical aircraft photos
│   ├── generate_patrol_map.py # Map generation script
│   └── requirements.txt
└── README.md
```

## Setup

### Prerequisites
- Python 3.10+
- MySQL 8.0+
- Google Cloud Vision API credentials (for OCR processing)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jmknapp/cod.git
   cd cod/patrolReports
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure the database:
   ```bash
   # Create .env file with your database credentials
   cat > .env << EOF
   DB_HOST=localhost
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_NAME=cod
   EOF
   ```

5. Initialize the database:
   ```bash
   mysql -u your_user -p < setup_database.sql
   ```

6. Run the application:
   ```bash
   python app.py
   ```

The application will be available at `http://localhost:5016`.

## Data Sources

- **Patrol Reports**: Digitized from National Archives records
- **Position Data**: Extracted from daily noon position reports in patrol logs
- **Ship/Aircraft Contacts**: Compiled from patrol report appendices
- **Glossary**: Compiled from WWII submarine terminology references

## Contributing

Contributions are welcome! Areas of interest:
- Additional patrol report transcription verification
- Historical research and fact-checking
- Map feature enhancements
- Accessibility improvements

## License

This project makes historical U.S. Navy documents accessible for educational purposes. The original patrol reports are public domain as U.S. government documents.

## Acknowledgments

- USS Cod Submarine Memorial, Cleveland, Ohio
- National Archives and Records Administration
- The officers and crew of USS Cod (SS-224)

---

*"Until dark tonight there seemed to be little doubt that we would at any moment find our missing shipmates. They were, individually, and as a group, experienced, capable and full of common sense."*  
— USS Cod patrol log, August 2, 1945


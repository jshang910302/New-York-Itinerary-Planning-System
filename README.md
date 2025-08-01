# New York Itinerary Planning System

## 🚀 Project Overview

A travel planning application that generates a personalized New York itinerary based on user inputs:

* **Duration** (per borough)
* **Total budget** and allocation ratios (attractions, dining, lodging)
* **Preference algorithm** (by rating, review count, or popularity index)

Users receive day-by-day recommendations for attractions, restaurants, and accommodations, all within budget and optimized for minimal transit time.

---

## 📂 Repository Structure

```text
/data_scraping/       # Web scraping notebooks
  ├── google_maps_scraper.ipynb    # Attractions & restaurant crawler
  └── booking_scraper.ipynb        # Accommodation crawler
/algorithm/           # Data cleaning & itinerary algorithms
  ├── clean_hotels.ipynb           # Hotel data processing & popularity index
  ├── clean_restaurants.ipynb      # Restaurant pricing & operational hours
  ├── clean_attractions.ipynb      # Attraction cost & subarea assignment
  └── itinerary_algorithm.ipynb    # Scheduling logic per user preferences
/frontend/            # User Interface (Tkinter GUI)
  ├── main.py                      # Launches T.A.I.N. application
  └── requirements.txt             # Python dependencies
/docs/                # Supplementary figures & report excerpts
README.md              # This file
```

---

## ⚙️ Backend Deliverables

### 🌐 Web Scraping

* **Google Maps Crawler**
  Automates searches across five boroughs (The Bronx, Brooklyn, Manhattan, Queens, Staten Island) to extract names, ratings, reviews count, pricing tiers, postcodes, and operating hours for attractions and restaurants.
* **Booking.com Crawler**
  Harvests lodging details—hotel names, prices, ratings, and user reviews—from Booking.com listings for all five boroughs.

### 🧮 Algorithm & Data Processing

1. **Input Validation**
   Ensures numeric budgets, 100% allocation ratio, and non-zero total days.
2. **Metro Fare & Budget Allocation**
   Applies NYC Metro 7‑day pass logic (≤7 days: \$1000; >7 days: \$2000) and divides remaining budget among categories and boroughs.
3. **Data Cleaning & Feature Engineering**

   * Hotels: computes popularity index = rating × review count, filters by budget, top‑3 recommendations per borough.
   * Restaurants: converts price tiers (\$ to \$\$\$\$) into numeric values, flags lunch availability, subdivides boroughs into A/B zones by zipcode.
   * Attractions: handles free vs. paid entries, assigns subareas, computes popularity index.
4. **Itinerary Scheduling**
   Alternates attractions and dining slots, respects subarea grouping to minimize transit, omits duplicates, and outputs per‑day plans.
5. **Results Export**
   Outputs transport cost, recommended accommodations, detailed daily itinerary with costs, ordered by Queens → Bronx → Manhattan → Brooklyn → Staten Island.

---

## 🎨 Frontend Deliverables

* **Tkinter GUI (T.A.I.N.)**

  * Uses `ttk` Aqua theme with `florawhite` background
  * Input widgets: text fields, spinboxes (0–3 days), comboboxes (preference selection)
  * Validation pop‑ups for incorrect inputs
  * **Submit** triggers backend pipeline and displays:

    * Metro fare
    * Recommended lodgings (or status messages)
    * Daily itinerary with attraction/restaurant names and costs

---

## 🛠️ Installation & Usage

1. **Clone Repository**

   ```bash
   git clone https://github.com/<username>/ny-itinerary-planner.git
   cd ny-itinerary-planner
   ```
2. **Backend Dependencies**
   *(for Jupyter notebooks and scraping)*

   ```bash
   pip install -r frontend/requirements.txt
   pip install selenium pandas openpyxl beautifulsoup4
   ```
3. **Launch GUI**

   ```bash
   python frontend/main.py
   ```
4. **Follow On‑Screen Prompts** to enter budget, days, and preference; click **Submit** to view your customized itinerary.

---

## 🤝 Contributing

1. Fork the repo 📂
2. Create a branch (`git checkout -b feature/xyz`)
3. Commit your changes (`git commit -m "Add xyz"`)
4. Push to branch (`git push origin feature/xyz`)
5. Open a Pull Request 🔀

---

## 📜 License

This project is licensed under MIT License. See [LICENSE](LICENSE) for details.

---

# 🎵 Personalized Music Discovery

## 📝 Description

Personalized Music Discovery is a web application that allows users to create customized Spotify playlists based on their choice of genres and music features. The created playlist is embedded into the web app and can also be added to the user's profile. The backend is powered by FastAPI with OAuth2 authentication handling with the Spotify API, while the frontend uses Flask and uvicorn to connect to simple HTML, CSS, and JavaScript.

## 🌟 Features

- **Search and Customize Playlists:** Users can search for playlists based on keywords, genres, or specific music features.
- **View Playlist Details:** Detailed information about each playlist, including track lists and features, is provided.
- **Save Playlists:** Logged-in users can save playlists to their account for later access.
- **OAuth2 Authentication with Spotify API:** Secure user authentication is handled using OAuth2 with the Spotify API.
- **Dynamic Frontend:** The frontend is dynamic, allowing users to interact with playlists and features seamlessly.
- **FastAPI Backend:** Efficient backend powered by FastAPI for handling API requests.
- **Error Handling:** Proper error handling and custom logging are implemented throughout the application.

## 💻 Technologies Used

- **Backend:** FastAPI (Python), Flask
- **Frontend:** HTML, CSS, JavaScript

## 🛠️ Setup Instructions

1. Clone the repository to your local machine.
2. Install the necessary dependencies using `pip install -r requirements.txt`.
3. Set up OAuth2 authentication handling with the Spotify API for the backend.
4. Run the backend server using `uvicorn main:app --reload`.
5. Access the application through your web browser.

## 🚀 Usage

1. **Search for Playlists:** Enter genres and specific music features into the search bar to create a custom playlist.
2. **Play/ Save Playlist Details:** You can play the playlist or also save it to your profile.

## 🎓 Takeaways and Challenges

Throughout the development process, we encountered challenges and gained valuable insights:

- **OAuth2 Integration:** Implementing OAuth2 authentication with the Spotify API provided a deeper understanding of secure authentication methods and API integration practices.

- **API Integration Complexity:** Integrating with the Spotify API for playlist customization deepened our understanding of API integration complexities and the significance of data consistency and accuracy.

- **Custom Module Development:** Building custom modules for interacting with the Spotify API, including OAuth2 token management, enhanced our proficiency in modular code design and API interaction.

- **Data Cleaning:** Conducting data cleaning and utilizing cleaned data for analysis provided insights into data preprocessing techniques and the importance of data quality for accurate analysis.

## Libraries and Frameworks Used

- **FastAPI**: Used as the backend web framework for handling API requests.
- **Flask**: Used for connecting the backend to simple HTML, CSS, and JavaScript for the frontend.
- **uvicorn**: Used for running the backend server.
- **pandas**: Used for data manipulation and analysis, particularly for cleaning the dataset.
- **numpy**: Used for numerical computing and handling arrays.
- **matplotlib**: Used for data visualization and plotting graphs.
- **Jinja2**: Used as the template engine for Flask to render HTML templates.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

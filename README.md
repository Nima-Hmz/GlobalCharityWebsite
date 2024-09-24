# GlobalCharityWeb

## Description
This project is a Django-powered charity donation platform that allows users to donate in multiple currencies.
Donations are automatically converted to a gold value using third-party currency conversion APIs, ensuring accurate and real-time conversion rates.
<br>
Users are then ranked based on the total amount of gold they have donated, fostering a sense of competition and community engagement.
<br>
This platform was built to simplify global donations for charities by offering multi-currency support and an engaging ranking system.
<br>
The use of API-powered currency conversions adds reliability and transparency to the donation process, creating an innovative way to measure contributions through gold value.
We have used the Navasan.net API for real-time currency conversion.

## Features
Multi-currency support: Users can donate using various currencies, which are converted to a universal gold value.
Gold-based ranking system: Donations are converted into gold using real-time exchange rates from external APIs, and users are ranked based on their total gold contributions.
<br>
Leaderboards: Displays a public ranking of top donors by gold value to encourage participation.
API integration: Utilizes reliable third-party APIs to ensure accurate currency-to-gold conversions.
User-friendly design: Intuitive interface for seamless donation experience.

## Installation
1) Clone the repository:
   ```git clone https://github.com/Nima-Hmz/XO_justforfun.git```

2) make sure you have python3 installed on your computer then install dependencies in project directory:
  ```python3 -m pip install -r requirments.txt```

## Usage
To run the donation platform on a localhost, follow these steps:
<br>
1) Navigate to the donate directory:
```cd donate```
2) Run the following command to start the application:
```python3 manage.py runserver```

## Contributing
Feel free to fork this project and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the GNU General Public License v3.0. For more details, see the LICENSE file.

## Contact
Created by [Nima-Hmz] - [hmznima77@gmail.com]

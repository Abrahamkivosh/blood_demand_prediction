# Blood Demand Prediction System

![Blood Demand Prediction System](https://daxg39y63pxwu.cloudfront.net/images/blog/predictive-analytics-in-healthcare-projects/Predictive_Analytics_in_Healthcare_Projects.png)

The Blood Demand Prediction System is a web application developed using the Django framework. This system aims to predict the demand for blood in different regions based on historical data and other relevant factors. The prediction can help blood banks and healthcare organizations to proactively manage their blood inventory and ensure an adequate supply of blood products for emergencies and regular medical needs.

## Features

- Predicts the demand for blood products in specific regions.
- Provides insights into historical blood demand patterns.
- User-friendly interface for data input and visualization.
- Admin dashboard for managing user access and system settings.

## Installation

Follow these steps to set up the Blood Demand Prediction System:

1. Clone the repository:

```bash
git clone https://github.com/your-username/blood-demand-prediction.git
```

2. Change directory:

```bash
cd blood-demand-prediction
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run database migrations:

```bash
python manage.py migrate
```

5. Create a superuser for accessing the admin dashboard:

```bash
python manage.py createsuperuser
```

6. Start the development server:

```bash
python manage.py runserver
```

7. Access the application in your web browser at `http://localhost:8000`.

## Usage

1. Login as an admin using the superuser credentials at `http://localhost:8000/admin/`.

2. Add users and configure system settings as needed.

3. Access the Blood Demand Prediction System at `http://localhost:8000/prediction/`.

4. The system is using current weather API to fetch current Weather data for four days forecasting.

5. Submit the region or city that you need to get weather forecasting and blood demand.

## Contributing

We welcome contributions to the Blood Demand Prediction System. If you find any issues or have ideas for improvements, please feel free to open an issue or submit a pull request. We appreciate your help in making this project better!

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- Thanks to the Django community for providing an excellent web framework.

## Contact

If you have any questions or inquiries, please feel free to contact us at [abrahamkivosh@gmail.com].

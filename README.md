# Train Times
A small script to pull train times from the Transport API and email them in a easy to read format.

## Prerequisites
- [Transport API Token](https://www.transportapi.com/)
- AWS SES Access/Secret Key
- Install `requirements.txt`
- (Optional) Completed `.env` file with the following:

  ```
  # Save as .env in the main directory
  
  app_id=""
  app_key=""
  SES_REGION_NAME=""
  AWS_ACCESS_KEY_ID=""
  AWS_SECRET_ACCESS_KEY=""
  SES_EMAIL_SOURCE=""
  SES_EMAIL_DEST=""
  ```

## Run the script
Call the file with two arguments. First the departure station, then the planned destination. Both have to be in the standard 3 letter alpha code, i.e Waterloo is WAT. A list of these codes can be found [here](https://www.nationalrail.co.uk/stations_destinations/48541.aspx).

For example running:

```python3 main.py eus man```


Will send the following email:

![](https://i.imgur.com/QdpnUSt.png)


## Example Usage
I personally have set this script to run twice a day with Windows Task Scheduler, once in the morning for my train to work and once in the evening for my train home. This gives me a heads up of any delays I may need to know about and lets me plan accordingly.

## Authors

* **Richard Tatum** - *Whole project* - [RichardTatum](https://github.com/richardtatum)


## License

This project is licensed under the MIT License.


## Acknowledgments

* Inspired by Chris Hutchinson and his awesome [train-departure-screen](https://github.com/chrishutchinson/train-departure-screen) project.

## Known Issues
Neither the API nor the script support journeys that require changing at a station. So something like WAT (London Waterloo) to MAN (Manchester Picadilly) will just return an error. Use something like [CityMapper](https://citymapper.com/) as it is much better suited to this!

# The DCA Experiment

This script uses a Google Sheet (via GCP) that contains the cost basis details for the "The DCA Experiment" portfolio to calculate the real-time portfolio performance. It then formats a breakdown of this performance and uses the Twitter API to send a Tweet on the @JacbWright Twitter account. Intended use is automating a manual process and creating transparency for the experiment's duration. Read a more thorough breakdown at https://jacb.dev/portfolio/dcaexperiment/.

Script is hosted on https://www.pythonanywhere.com/ and uses it's scheduler to run every day at 4PM MST. Utilizes the following Google Sheet for cost-basis tracking: https://docs.google.com/spreadsheets/d/1k_xaCGcDtKTTZ1B9cjeUWxv3PxN5jLC1jSWFybYcvhc/edit?usp=sharing.

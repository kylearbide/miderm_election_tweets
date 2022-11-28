# Twitter project on Midterm Election 2022

The following repository is our entire analysis of twitter data collected around and about the 2022 Midterm Election. The entire analysis is conducted in Python, with an interface created using Streamlit. The dataset and pre-trained models are quite large, so to access them please reach out to me directly at kylearbide@gwu.edu. 

**text_preproc.py**

Preprocessing file for our text data, all of the steps are broken down in the report as to what was included and why

**topic_modeling_BERTopic.ipynb**

This is the final notebook used to created the saved topic models for our analysis. Runtime for generating these models can be quite long so I don't recommend running these unless you have time and want to create your own models

**streamlit app**

The interface for our project. This calls the plots created in `topic_plotting.ipynb` but allows the user enhanced filters and customization. To run, install streamlit, navigate to this direction and enter the following in the command line

`streamlit run Welcom_Page.py`
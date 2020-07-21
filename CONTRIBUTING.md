# How to Contribute

We'd love to accept your patches and contributions to this project. There are
just a few small guidelines you need to follow.

## Contributor License Agreement

Contributions to this project must be accompanied by a Contributor License
Agreement. You (or your employer) retain the copyright to your contribution;
this simply gives us permission to use and redistribute your contributions as
part of the project. Head over to <https://cla.developers.google.com/> to see
your current agreements on file or to sign a new one.

You generally only need to submit a CLA once, so if you've already submitted one
(even if it was for a different project), you probably don't need to do it
again.

## Code reviews

All submissions, including submissions by project members, require review. We
use GitHub pull requests for this purpose. Consult
[GitHub Help](https://help.github.com/articles/about-pull-requests/) for more
information on using pull requests.

## Notebook contributions

To guarantee standardization for assets in Google repositories we have
put together some recommendations which will help Google provide
consistency and quality for the notebook assets:

Please make sure you follow the next steps when developing Notebooks:

   1. Clone and develop off of this notebook [templates](notebooks/templates)
   2. If notebook is meant as official documentation, work with techwriter on written content 
   3. Ensure notebook [requirements](#Notebook-requirements) are met
   4. Ensure notebook runs from top to bottom without errors
   5. Place the notebook in correct [location](#Notebooks-location)
   6. Run [nbfmt](#Notebook-formatting).
   7. Create a pull request in a relevant repository
   8. Reviewers provide feedback and work with you to merge pull request

 
   If Colab is required please provide compatibility with AI Platform
   Notebooks, to help you on this we have created a template for you!
   [Template here](notebooks/templates/ai_platform_notebooks_template_hybrid.ipynb)
   
   ## Notebook requirements
   1. Use [AI Platform notebooks](https://cloud.google.com/ai-platform-notebooks/)
   We highly recommend to guarantee that your Notebook runs in AI Platform Notebooks
   
   2. Use [templates](notebooks/templates) listed above. 
   3. Provide novel and relevant content 
   4. Provide Notebook documentation
   5. Use latest ML framework version
   6. Follow software engineering principles:
      - [Python style guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md)
      - Notebook code is [formatted](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/code_prettify/README_autopep8.html)
      - Use [Python 3.X](https://www.python.org/download/releases/3.0/)
      - Documentation      
      
   ## Notebook formatting
   
   ```
   # Install the tensorflow-docs package:
   $ python3 -m pip install -U git+https://github.com/tensorflow/docs

   # Format individual notebooks:
   $ python3 -m tensorflow_docs.tools.nbfmt ./path/to/notebook.ipynb [...]

   # Or a directory of notebooks:
   $ python3 -m tensorflow_docs.tools.nbfmt ./path/to/notebooks/
   ```
      
   ## Notebooks location
   
   Add your notebook to the following folder: ai-platform-samples > notebooks > samples:
   
   - AutoML Tables
   - BigQuery
   - BigQuery ML
   
   For the following products, select the ML framework and place it accordingly:
   
   - AI Platform Training
   - AI Platform Prediction
   - AI Platform Explanations
   - AI Platform Notebooks
   
   Directory structure:

         
         .
         ├── datasets
         └── notebooks
             └── samples
                 ├── automl
                 ├── bigquery
                 ├── bqml
                 ├── mxnet
                 ├── pytorch
                 ├── scikit-learn
                 └── tensorflow
                     └── census
                           └── tensorflow_census_getting_started.ipynb
         


## Community Guidelines

This project follows [Google's Open Source Community
Guidelines](https://opensource.google.com/conduct/).

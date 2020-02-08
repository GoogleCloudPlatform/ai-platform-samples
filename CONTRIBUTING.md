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

Use Notebook [templates](notebooks/templates)

-  Use
   [AI Platform notebooks](https://cloud.google.com/ai-platform-notebooks/):
   We highly recommend to guarantee that your Notebook runs in AI
   Platform notebooks
   [Template here](notebooks/templates/ai_platform_notebooks_template.ipynb).
   
   If Colab is required please provide compatibility with AI Platform
   notebooks, to help you on this we have created a template for you!
   [Template here]((notebooks/templates/ai_platform_notebooks_template_hybrid.ipynb)
   
   **Notebook Development Guidelines:**
   1. Use [templates](notebooks/templates) listed above. 
   2. Provide novel and relevant content 
   3. Documentation
   4. Asset is executable without errors 
   5. Use latest ML framework
   6. Follow Software engineering principles
      - Python 3.X
      - [Python style guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md)
      - Notebook code is
        [formatted](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/code_prettify/README_autopep8.html)
      - Documentation

-  We encourage you to verify your notebook executes without errors. If
   you need to use other notebook environment (e.g. Colab, Kaggle,
   Datalab, etc. we still encourage you to make sure the notebook is
   compatible with AI Platform Notebooks).

## Community Guidelines

This project follows [Google's Open Source Community
Guidelines](https://opensource.google.com/conduct/).

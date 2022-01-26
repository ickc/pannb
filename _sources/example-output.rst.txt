=======================
Pandoc filter for ipynb
=======================

:Author: Kolen Cheung

.. container:: cell markdown
   :name: fc4e8ae7-9d4d-42a4-a880-d5e5d9e11d2f

   .. rubric:: Example
      :name: example

   An example with some markdown texts.

   Compare `source <../example/>`__ and `output <../example-output/>`__.

   Below we'll write some Python code that will becomes invisible after
   pannb filtering.

.. container::
   :name: 3f02e5f1-d9a7-4645-9d3c-6d2914b2bc70

.. container:: cell markdown
   :name: d68cd8b4-a9a1-4b2b-85a3-2fa0c3ad9f35

   However, the HTML output of these cells should be visible, and
   converted to pandoc's internal format.

   For example, the below table will be valid in LaTeX output.

.. container::
   :name: 2efe6488-91e7-48d0-86c5-791c594a9340

   .. container::

      == = = =
      \  0 1 2
      == = = =
      0  0 1 2
      1  3 4 5
      2  6 7 8
      == = = =

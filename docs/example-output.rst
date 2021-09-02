=======================
Pandoc filter for ipynb
=======================

:Author: Kolen Cheung

.. container:: cell markdown

   .. rubric:: Example
      :name: example

   An example with some markdown texts.

   Compare `source <../example/>`__ and `output <../example-output/>`__.

   Below we'll write some Python code that will becomes invisible after
   pannb filtering.

.. container:: cell code

.. container:: cell markdown

   However, the HTML output of these cells should be visible, and
   converted to pandoc's internal format.

   For example, the below table will be valid in LaTeX output.

.. container:: cell code

   .. container:: output execute_result

      ::

            0  1  2
         0  0  1  2
         1  3  4  5
         2  6  7  8

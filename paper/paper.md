---
title: 'EleMap: A Web App for Custom Visualization of Periodic Table Properties'
tags:
  - Python
  - chemistry
  - periodic table
  - data visualization
  - Streamlit
  - materials science
authors:
  - name: Prince Sharma
    orcid: 0000-0001-5735-5206
    affiliation: "1"
  - name: Madhura Adeppady
    orcid: 0000-0001-5661-6662
    affiliation: "2"
affiliations:
  - name: Department of Mechanical Engineering and Mechanics, Lehigh University, Bethlehem, PA 18015, USA
    index: 1
  - name: Department of Electronics and Telecommunications, Politecnico di Torino, Italy
    index: 2
date: 2025-04-21
bibliography: ref.bib
---

# Summary

The periodic table is a cornerstone of chemistry and materials science, yet there is a lack of accessible, customizable digital visualization tools or robust code frameworks to support data presentation. Researchers and educators frequently need to visualize custom elemental datasets—such as experimental measurements, computational predictions, or machine-learned properties—on an periodic table.

**EleMap** is employing Streamlit-based Python web application that addresses these challenges. It enables users to upload CSV files containing element symbols and numerical properties, generating a dynamic, color-coded periodic table heatmap. With features like customizable group and period ranges, selectable color maps, exportable high-resolution images, and an intuitive web interface, PeriodicVis is a versatile tool for both research and education. Unlike previous solutions, it offers a robust, no-code platform for visualizing any numerical property, making it a significant tool for researchers and educators in the field.

# Statement of need

Visualizing periodic trends is essential for teaching chemistry and materials research. However, prior tools were constrained to standard properties (e.g., electronegativity, atomic radius) or demanded advanced coding skills to adapt for custom datasets. Researchers working with properties like formation energies, electronic band gaps, or other material descriptors often relied on complex workflows involving Python libraries such as matplotlib [@Hunter2007], pandas [@cKinney2010], and streamlit [@Streamlit2020]. No robust, user-friendly tool existed to seamlessly visualize arbitrary element-property datasets in a web-based environment.

**EleMap** bridges this gap by providing an intuitive, no-code solution. It accepts arbitrary element-property pairs, dynamically updates the layout and color scale, and supports export for publication-quality figures. The interface makes use of Streamlit’s rapid deployment framework, making it easy to use in-browser via local or cloud hosting. This tool will prove to be useful for educators wanting to demonstrate specific trends using custom values and researchers wanting to visualize materials data for publications.

# Functionality

Key features of `EleMap` include:
- Upload of CSV files with two columns: `Element`, and a user-defined numerical property.
- Custom selection of group range (1–18) and period range (1–7, including La/Ac).
- Dropdown menu to select any supported `matplotlib` color map.
- Export options: `PNG`, `SVG`, and `TIFF` at user-specified DPI (300–1200).
- Annotations of each element box with the element symbol and property value.

The app uses a 2D list to represent the periodic table layout, with La and Ac rows handled explicitly. Upon upload, the app validates data, maps it to the table layout, and creates a figure using `matplotlib`, complete with colorbar and annotations.

# Acknowledgements

Thanks to open-source projects including `Streamlit`, `matplotlib`, `pandas`, and the Python community.


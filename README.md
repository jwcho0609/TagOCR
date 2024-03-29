# Garment Tag Scanning and Sorting for Sustainability
Senior Capstone Design Project for categorizing clothing based on garment tag information
created by The Bee's Knees.

Project sponsored by [Celestial Theory](https://celestialtheory.com/) and advised by Dr. Itzhak Green.

## Executive Summary

62.5% of used textiles end up in landfills, and only 14.5% recyclable textiles are actually recycled [[1]](#ref1) just in the United States. With this issue in mind, Celestial Theory desires to create an assembly line that can take in recycled clothing and remanufacture the fibers in order to use them in new ways. Starting the process, Celestial Theory needs a device that sorts clothes based on the primary material before the recycling process can begin. The device will be used by an operator that scans the garment’s tag and puts it into the device for sorting. The device should be user-friendly and at its current stage, only focus on readable tags and not damaged or faded tags. However, a workaround should be created in order to keep up the flow of production.

Engaging challenges for this device are scanning garment tags accurately and sorting the clothes in their corresponding bins. A Raspberry Pi with an attached camera will read in the tags for scanning the garment tags. The camera has a focus range of 4–10mm and will be placed under an acrylic plate for its protection and to guide the scanning of the garment tag. The largest technical challenge is identifying the dominant material. Currently, the software can repeatedly identify the dominant material, and in the event of two materials being equally dominant, the first material analyzed is considered the dominant one. To correctly sort the clothes, the device will use a pipe assembly that is rotated by a motor and gears. The bottom of the pipe assembly will guide the clothes to their corresponding locations. This angle minimizes the effects of friction on the clothes and effectively transfers vertical kinetic energy to horizontal kinetic energy. A stepper motor was selected to rotate the pipe due to its simple open-loop position and speed control. The selected stepper motor provides 56.5 oz-in of torque and requires 4.8W of power. This torque and power meet the Celestial Theory’s specifications for the design. Celestial Theory’s other specifications include the weight and safety of the device. The current weight projection of the prototype is 16lbs which meets the OSHA requirement of 40 lbs or less for a device that can be carried. Following OSHA requirement 1910.219, the gears will be enclosed to eliminate the possibility of clothes getting jammed or potential injuries.

The end goal is for the machine to be as straightforward and user-friendly as possible while accurately scanning and efficiently sorting. Through testing and adjustments, the team aims to find the optimal motor speeds to match an operator’s pace. The device also will store the information of the clothes being fed through and be able to report the information to the operator.

### Refer to the [final report](https://drive.google.com/file/d/11VzxfLUv5NG98AHOf8EYxWWPzp5fr2s1/view?usp=sharing) for a more extensive report and the fabrication package. 

## Final Assembly

<img src="ReadmeImages/assemb.jpeg" width="250"><img src="ReadmeImages/scanner1.jpeg" width="250"><img src="ReadmeImages/scanner2.jpeg" width="250">

## Demonstration

<img src="ReadmeImages/demo.gif" width="800">
<!-- ![Demo video](ReadmeImages/demo.gif) -->

## References

<a name="ref1"></a> [1] “SMART,” Frequently Asked Questions. [Online] Available: https://www.smartasn.org/resources/frequently-asked-questions/

# XML
XML stands for Extensible Markup Language
* storing data records that are fully platform independent
* markup language same as html
* Customised user defined tags for storing data
* Xml just store data temporarily or permanently
* Data can be inserted or updated into database tables 

XML is used for rendering or connecting an application and database.

## XML structure
Xml has only one root element and starts from top. XML has a tree structure of data. Tree structure has one root, child elements, branches, attributes, values.

XML can create customized nested tags to maintain tree structure.

```
<employee>
  <emp_info id="1">
    <name>
      <first_name>Opal</first_name>
      <middle_name>Venue</middle_name>
      <last_name>Kole</last_name>
    </name>
    <contact_info>
      <company_info>
        <comp_name>Odoo (formally OpenERP)</comp_name>
        <comp_location>
          <street>Tower-1, Infocity</street>
          <city>GH</city>
          <phone>000-478-1414</phone>
        </comp_location>
        <designation>Junior Engineer</designation>
      </company_info>
    <phone>000-987-4745</phone>
    <email>email@myemail.com</email>
    </contact_info>
  </emp_info>
</employee>
```

<div style="text-align:center"><img src="./images/xml_tree_structure.png" 
alt="XML tree structure" border="1" /></div>


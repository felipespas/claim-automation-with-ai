-- SELECT * FROM SalesLT.Product
-- SELECT * FROM SalesLT.ProductCategory
-- SELECT * FROM SalesLT.ProductModel
-- SELECT * FROM SalesLT.ProductModelProductDescription
-- SELECT * FROM SalesLT.ProductDescription

SELECT 
    OrderDate, 
    SOH.SalesOrderID, 
    SOH.SubTotal,
    SOH.TaxAmt,
    SOH.TotalDue,
    SOH.ShipMethod,
    FirstName, 
    MiddleName, 
    LastName, 
    C.SalesPerson,
    P.Name,
    P.Color,
    SOD.OrderQty, 
    SOD.UnitPrice, 
    SOD.LineTotal,
    A.*
FROM SalesLT.SalesOrderHeader SOH
INNER JOIN SalesLT.Customer C
ON SOH.CustomerID = C.CustomerID
INNER JOIN SalesLT.SalesOrderDetail SOD
ON SOH.SalesOrderID = SOD.SalesOrderID
INNER JOIN SalesLT.Product P
ON SOD.ProductID = P.ProductID
INNER JOIN SalesLT.Address A
ON SOH.ShipToAddressID = A.AddressID
WHERE SOH.SalesOrderID = 71780

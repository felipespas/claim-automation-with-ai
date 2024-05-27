CREATE OR ALTER PROCEDURE p_ReturnProductData(@ProductId INT)
AS
BEGIN
    SELECT * FROM SalesLT.Product WHERE ProductId = @ProductId
    FOR JSON AUTO
END
GO

EXEC p_ReturnProductData 680
GO

CREATE OR ALTER PROCEDURE p_ReturnOrderData(@OrderId INT)
AS
BEGIN
    SELECT 
        SOH.OrderDate, 
        SOH.SalesOrderID, 
        SOH.SubTotal,
        SOH.TaxAmt,
        SOH.TotalDue,
        SOH.ShipMethod,
        C.FirstName, 
        C.MiddleName, 
        C.LastName, 
        C.SalesPerson,
        P.Name AS ProductName,
        P.Color AS ProductColor,
        SOD.OrderQty AS ProductQuantity, 
        SOD.UnitPrice AS ProductUnitPrice, 
        SOD.LineTotal AS ProductLineTotal
    FROM SalesLT.SalesOrderHeader SOH
    INNER JOIN SalesLT.Customer C
    ON SOH.CustomerID = C.CustomerID
    INNER JOIN SalesLT.SalesOrderDetail SOD
    ON SOH.SalesOrderID = SOD.SalesOrderID
    INNER JOIN SalesLT.Product P
    ON SOD.ProductID = P.ProductID
    INNER JOIN SalesLT.Address A
    ON SOH.ShipToAddressID = A.AddressID
    WHERE SOH.SalesOrderID = @OrderId
END
GO

EXEC p_ReturnOrderData 71780
GO

CREATE OR ALTER PROCEDURE p_ReturnOrderData_JSON(@OrderId INT)
AS
BEGIN
    SELECT TOP 1
        SOH.OrderDate, 
        SOH.SalesOrderID, 
        SOH.SubTotal,
        SOH.TaxAmt,
        SOH.TotalDue,
        SOH.ShipMethod,
        C.FirstName, 
        C.MiddleName, 
        C.LastName, 
        C.SalesPerson,
        P.Name AS ProductName,
        P.Color AS ProductColor,
        SOD.OrderQty AS ProductQuantity, 
        SOD.UnitPrice AS ProductUnitPrice, 
        SOD.LineTotal AS ProductLineTotal
    FROM SalesLT.SalesOrderHeader SOH
    INNER JOIN SalesLT.Customer C
    ON SOH.CustomerID = C.CustomerID
    INNER JOIN SalesLT.SalesOrderDetail SOD
    ON SOH.SalesOrderID = SOD.SalesOrderID
    INNER JOIN SalesLT.Product P
    ON SOD.ProductID = P.ProductID
    INNER JOIN SalesLT.Address A
    ON SOH.ShipToAddressID = A.AddressID
    WHERE SOH.SalesOrderID = @OrderId
    FOR JSON AUTO
END
GO

EXEC p_ReturnOrderData_JSON 71780
GO

CREATE OR ALTER PROCEDURE p_ReturnOrderProducts_JSON(@OrderId INT)
AS
BEGIN
    SELECT        
        P.Name AS ProductName        
    FROM SalesLT.SalesOrderHeader SOH
    INNER JOIN SalesLT.SalesOrderDetail SOD
    ON SOH.SalesOrderID = SOD.SalesOrderID
    INNER JOIN SalesLT.Product P
    ON SOD.ProductID = P.ProductID
    WHERE SOH.SalesOrderID = @OrderId
    FOR JSON AUTO
END
GO

EXEC p_ReturnOrderProducts_JSON 71780
GO
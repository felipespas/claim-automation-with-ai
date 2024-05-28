CREATE OR ALTER PROCEDURE p_ReturnOrderDetails_JSON(@OrderId INT)
AS
BEGIN
    SELECT CAST((
        SELECT 
            SOH.SalesOrderID AS OrderId,
            SOH.OrderDate AS OrderDate,
            C.FirstName + ' ' + C.MiddleName +  ' ' + C.LastName AS CustomerFullName,
            SOH.TaxAmt AS TaxAmount,
            SOH.Freight AS Freight,
            SOH.TotalDue AS TotalDue,
            (
                SELECT
                    P.Name AS ProductName,
                    SOD.OrderQty AS Quantity,
                    SOD.UnitPrice AS UnitPrice,
                    SOD.LineTotal AS TotalPrice
                FROM SalesLT.SalesOrderDetail SOD
                INNER JOIN SalesLT.Product P
                ON SOD.ProductID = P.ProductID
                WHERE SOH.SalesOrderID = SOD.SalesOrderID
                FOR JSON PATH
            ) AS Products
        FROM SalesLT.SalesOrderHeader SOH
        INNER JOIN SalesLT.Customer C
        ON SOH.CustomerID = C.CustomerID
        WHERE SOH.SalesOrderID = @OrderId
        FOR JSON PATH
    ) AS NVARCHAR(MAX)) AS Result
END
GO

EXEC p_ReturnOrderDetails_JSON 71780
GO
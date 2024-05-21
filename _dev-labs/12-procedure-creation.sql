CREATE OR ALTER PROCEDURE p_ReturnProductData(@ProductId INT)
AS
BEGIN
    SELECT * FROM SalesLT.Product WHERE ProductId = @ProductId
    FOR JSON AUTO
END
GO

EXEC p_ReturnProductData 680
GO
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[tblStockCategory](
	[categoryname] [nvarchar](64) NULL,
	[Stockname] [nvarchar](64) NULL,
	[Stockid] [varchar](32) NULL,
	[EntryDate] [datetime2](0) NULL
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[tblStockCategory] ADD  CONSTRAINT [dftime]  DEFAULT (getdate()) FOR [EntryDate]
GO

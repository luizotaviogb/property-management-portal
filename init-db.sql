DROP TABLE IF EXISTS maintenance;
DROP TABLE IF EXISTS leases;
DROP TABLE IF EXISTS tenants;
DROP TABLE IF EXISTS properties;
DROP TABLE IF EXISTS property_types;
DROP TABLE IF EXISTS property_statuses;
DROP TABLE IF EXISTS maintenance_statuses;
DROP TABLE IF EXISTS payment_statuses;

CREATE TABLE property_statuses (
    PropertyStatusID SERIAL PRIMARY KEY,
    Description VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE maintenance_statuses (
    MaintenanceStatusID SERIAL PRIMARY KEY,
    Description VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE payment_statuses (
    PaymentStatusID SERIAL PRIMARY KEY,
    Description VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE property_types (
    PropertyTypeID SERIAL PRIMARY KEY,
    Description VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE properties (
    PropertyID SERIAL PRIMARY KEY,
    Address VARCHAR(255) NOT NULL,
    PropertyTypeID INTEGER NOT NULL,
    PropertyStatusID INTEGER NOT NULL,
    PurchaseDate DATE NOT NULL,
    Price DECIMAL(15, 2) NOT NULL CHECK (Price >= 0),
    CONSTRAINT fk_property_type FOREIGN KEY (PropertyTypeID) REFERENCES property_types(PropertyTypeID) ON DELETE RESTRICT,
    CONSTRAINT fk_property_status FOREIGN KEY (PropertyStatusID) REFERENCES property_statuses(PropertyStatusID) ON DELETE RESTRICT
);

CREATE TABLE tenants (
    TenantID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    ContactInfo VARCHAR(100) NOT NULL
);

CREATE TABLE leases (
    LeaseID SERIAL PRIMARY KEY,
    TenantID INTEGER NOT NULL,
    PropertyID INTEGER NOT NULL,
    LeaseTermStart DATE NOT NULL,
    LeaseTermEnd DATE NOT NULL,
    PaymentStatusID INTEGER NOT NULL,
    CONSTRAINT fk_tenant FOREIGN KEY (TenantID) REFERENCES tenants(TenantID) ON DELETE RESTRICT,
    CONSTRAINT fk_property FOREIGN KEY (PropertyID) REFERENCES properties(PropertyID) ON DELETE RESTRICT,
    CONSTRAINT fk_payment_status FOREIGN KEY (PaymentStatusID) REFERENCES payment_statuses(PaymentStatusID) ON DELETE RESTRICT,
    CONSTRAINT valid_lease_dates CHECK (LeaseTermEnd > LeaseTermStart)
);

CREATE TABLE maintenance (
    TaskID SERIAL PRIMARY KEY,
    Description TEXT NOT NULL,
    MaintenanceStatusID INTEGER NOT NULL,
    ScheduledDate DATE NOT NULL,
    PropertyID INTEGER NOT NULL,
    CONSTRAINT fk_maintenance_status FOREIGN KEY (MaintenanceStatusID) REFERENCES maintenance_statuses(MaintenanceStatusID) ON DELETE RESTRICT,
    CONSTRAINT fk_property FOREIGN KEY (PropertyID) REFERENCES properties(PropertyID) ON DELETE RESTRICT
);

ALTER SEQUENCE property_statuses_PropertyStatusID_seq RESTART WITH 1;
ALTER SEQUENCE maintenance_statuses_MaintenanceStatusID_seq RESTART WITH 1;
ALTER SEQUENCE payment_statuses_PaymentStatusID_seq RESTART WITH 1;
ALTER SEQUENCE property_types_PropertyTypeID_seq RESTART WITH 1;
ALTER SEQUENCE properties_PropertyID_seq RESTART WITH 1;
ALTER SEQUENCE tenants_TenantID_seq RESTART WITH 1;
ALTER SEQUENCE leases_LeaseID_seq RESTART WITH 1;
ALTER SEQUENCE maintenance_TaskID_seq RESTART WITH 1;

INSERT INTO property_statuses (Description) VALUES
('Vacant'),
('Occupied'),
('Under Maintenance');

INSERT INTO maintenance_statuses (Description) VALUES
('Completed'),
('In Progress'),
('Pending');

INSERT INTO payment_statuses (Description) VALUES
('Paid'),
('Pending'),
('Overdue');

-- Inserir dados em property_types
INSERT INTO property_types (Description) VALUES
('Residential'),
('Commercial'),
('Other');

INSERT INTO properties (Address, PropertyTypeID, PropertyStatusID, PurchaseDate, Price) VALUES
('12 Rue des Lilas, Paris, 75015', 1, 1, '2020-06-15', 350000.00), -- Residential, Vacant
('8 Avenue Foch, Lyon, 69006', 2, 2, '2019-11-30', 950000.00),    -- Commercial, Occupied
('3 Quai de Grenelle, Marseille, 13002', 1, 2, '2021-01-20', 400000.00); -- Residential, Occupied

INSERT INTO tenants (Name, ContactInfo) VALUES
('Jean Dupont', '+33123456789'),
('Marie Curie', '+33456789012'),
('Claude Monet', '+33789012345');

INSERT INTO leases (TenantID, PropertyID, LeaseTermStart, LeaseTermEnd, PaymentStatusID) VALUES
(1, 3, '2022-05-01', '2023-04-30', 1),
(2, 2, '2023-01-15', '2024-01-14', 2),
(3, 2, '2022-07-10', '2023-07-09', 1);

INSERT INTO maintenance (Description, MaintenanceStatusID, ScheduledDate, PropertyID) VALUES
('Fix leaking roof', 1, '2022-03-15', 1),       -- Completed
('Repaint exterior walls', 2, '2023-02-20', 3), -- In Progress
('Update security system', 3, '2023-04-05', 2); -- Pending

CREATE INDEX idx_properties_propertytypeid ON properties(PropertyTypeID);
CREATE INDEX idx_properties_propertystatusid ON properties(PropertyStatusID);
CREATE INDEX idx_leases_tenantid ON leases(TenantID);
CREATE INDEX idx_leases_propertyid ON leases(PropertyID);
CREATE INDEX idx_leases_paymentstatusid ON leases(PaymentStatusID);
CREATE INDEX idx_maintenance_propertyid ON maintenance(PropertyID);
CREATE INDEX idx_maintenance_maintenancestatusid ON maintenance(MaintenanceStatusID);
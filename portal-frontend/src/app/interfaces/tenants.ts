export interface ITenant {
  id: number;
  name: string;
  contactInfo: string;
  leaseTermStart: string;
  leaseTermEnd: string;
  paymentStatus: string;
  propertyId: number;
}
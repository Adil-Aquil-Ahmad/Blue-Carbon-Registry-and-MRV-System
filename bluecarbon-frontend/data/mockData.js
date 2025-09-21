/* Put the dataset you shared here. Export named exports for projects, users, credits etc. */

export const projects = [
  {
    id: 'BC001',
    name: 'Sundarbans Mangrove Restoration',
    location: 'West Bengal, India',
    coordinates: [21.9497, 88.7879],
    status: 'verified',
    hectares: 150,
    creditsMinted: 2500,
    submittedDate: '2024-01-15',
    verifiedDate: '2024-02-01',
    organization: 'West Bengal Forest Department',
    description: 'Large-scale mangrove restoration project in the Sundarbans delta region.',
    images: [
      'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&q=80',
      'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80'
    ]
  },
  {
    id: 'BC002',
    name: 'Kerala Coastal Wetland Conservation',
    location: 'Kerala, India',
    coordinates: [9.9312, 76.2673],
    status: 'pending',
    hectares: 75,
    creditsMinted: 0,
    submittedDate: '2024-02-10',
    verifiedDate: null,
    organization: 'Kerala State Biodiversity Board',
    description: 'Coastal wetland restoration and conservation project.',
    images: [
      'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80'
    ]
  },
  {
    id: 'BC003',
    name: 'Gujarat Salt Marsh Restoration',
    location: 'Gujarat, India',
    coordinates: [23.0225, 72.5714],
    status: 'in-progress',
    hectares: 200,
    creditsMinted: 1200,
    submittedDate: '2024-01-20',
    verifiedDate: '2024-02-15',
    organization: 'Gujarat Ecology Commission',
    description: 'Salt marsh restoration project along the Gujarat coastline.',
    images: ['https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80']
  },
  {
    id: 'BC004',
    name: 'Tamil Nadu Seagrass Conservation',
    location: 'Tamil Nadu, India',
    coordinates: [11.1271, 78.6569],
    status: 'verified',
    hectares: 90,
    creditsMinted: 1800,
    submittedDate: '2024-01-05',
    verifiedDate: '2024-01-25',
    organization: 'Tamil Nadu Forest Department',
    description: 'Seagrass bed conservation and restoration project.',
    images: [
      'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&q=80',
      'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80'
    ]
  }
]

export const users = {
  'field-worker': { id:'1', name:'Rajesh Kumar', role:'field-worker', email:'rajesh.kumar@example.com' },
  ngo: { id:'2', name:'Dr. Priya Sharma', role:'ngo', email:'priya.sharma@example.com' },
  'nccr-admin': { id:'3', name:'Amit Patel', role:'nccr-admin', email:'amit.patel@nccr.gov.in' }
}

export const credits = [
  { id:'CC001', projectId:'BC001', amount:2500, mintedDate:'2024-02-01', status:'active', price:15.5, buyer:'Carbon Solutions Ltd.' }
]

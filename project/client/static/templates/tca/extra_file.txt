import ComposableArchitecture
import Foundation


public struct Transaction: Identifiable, Equatable {
    public var id: String { alias.reference }

    // example: "REWE Group"
    public let partnerDisplayName: String
    public let alias: Alias
    // example: 1
    // Must be an enum
    public let category: Category
    public let detail: Detail
    
    public init(partnerDisplayName: String, alias: Alias, category: Category, detail: Detail) {
        self.partnerDisplayName = partnerDisplayName
        self.alias = alias
        self.category = category
        self.detail = detail
    }
    
    public struct Alias: Equatable {
        // example: "795357452000810"
        public let reference: String
        
        public init(reference: String) {
            self.reference = reference
        }
    }
    
    public struct Detail: Equatable {
        // example: "Punkte sammeln"
        public let description: String?
        // example: "2022-07-24T10:59:05+0200"
        public let bookingDate: Date
        
        public let value: Value
        
        public init(description: String?, bookingDate: Date, value: Value) {
            self.description = description
            self.bookingDate = bookingDate
            self.value = value
        }
        
        public struct Value: Equatable {
            // example: 124
            public let amount: Double
            // example: PBP
            public let currency: String
            
            public init(amount: Double, currency: String) {
                self.amount = amount
                self.currency = currency
            }
        }
    }
    
    public enum Category: Int, Equatable, CaseIterable, Identifiable {
        public var id: Int { self.rawValue }
        
        case all = 0
        case category1 = 1
        case category2 = 2
        case category3 = 3
    }
}

//extension Transaction.Category: Pickable {
//    var text: String {
//        switch self {
//        case .all:
//            return Localizables.allCategories.text
//        case .category1:
//            return Localizables.category1.text
//        case .category2:
//            return Localizables.category2.text
//        case .category3:
//            return Localizables.category3.text
//        }
//    }
//}

extension TransactionModule.State: Identifiable {
    public var id: String {
        self.transaction.alias.reference
    }
    
    
}

extension Transaction: Codable {
    public enum CodingKeys: String, CodingKey {
        case partnerDisplayName
        case alias
        case category
        case detail = "transactionDetail"
    }
}

extension Transaction.Detail: Codable {}
extension Transaction.Detail.Value: Codable {}
extension Transaction.Alias: Codable {}
extension Transaction.Category: Codable {}


public enum TransactionSortDirection: String, CaseIterable {
    case bookingDateDesc
    case bookingDateAsc
    case amountDesc
    case amountAsc
}